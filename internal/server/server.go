package server

import (
	"encoding/json"
	"errors"
	"net/http"
	"strconv"
	"strings"

	"academic-codebase/goapi/internal/books"
)

// Server exposes HTTP handlers for the API.
type Server struct {
	store *books.Store
}

// New creates a new Server instance.
func New(store *books.Store) *Server {
	return &Server{store: store}
}

// Routes builds the HTTP handler tree for the API.
func (s *Server) Routes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/health", s.handleHealth)
	mux.HandleFunc("/books", s.handleBooks)
	mux.HandleFunc("/books/", s.handleBookByID)
	return loggingMiddleware(mux)
}

func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

func (s *Server) handleBooks(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		s.listBooks(w, r)
	case http.MethodPost:
		s.createBook(w, r)
	default:
		writeError(w, http.StatusMethodNotAllowed, "method not allowed")
	}
}

func (s *Server) handleBookByID(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeError(w, http.StatusMethodNotAllowed, "method not allowed")
		return
	}

	idStr := strings.TrimPrefix(r.URL.Path, "/books/")
	if idStr == "" {
		writeError(w, http.StatusNotFound, "book not found")
		return
	}

	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		writeError(w, http.StatusBadRequest, "invalid book id")
		return
	}

	book, err := s.store.Get(id)
	if errors.Is(err, books.ErrNotFound) {
		writeError(w, http.StatusNotFound, "book not found")
		return
	}
	if err != nil {
		writeError(w, http.StatusInternalServerError, "could not load book")
		return
	}

	writeJSON(w, http.StatusOK, book)
}

func (s *Server) listBooks(w http.ResponseWriter, r *http.Request) {
	books := s.store.List()
	writeJSON(w, http.StatusOK, map[string]any{"items": books})
}

func (s *Server) createBook(w http.ResponseWriter, r *http.Request) {
	var payload struct {
		Title  string `json:"title"`
		Author string `json:"author"`
	}

	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		writeError(w, http.StatusBadRequest, "invalid JSON payload")
		return
	}

	payload.Title = strings.TrimSpace(payload.Title)
	payload.Author = strings.TrimSpace(payload.Author)

	if payload.Title == "" || payload.Author == "" {
		writeError(w, http.StatusBadRequest, "title and author are required")
		return
	}

	book := s.store.Create(payload.Title, payload.Author)
	writeJSONWithStatus(w, http.StatusCreated, book)
}

func writeJSON(w http.ResponseWriter, status int, v any) {
	writeJSONWithStatus(w, status, v)
}

func writeJSONWithStatus(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}

func writeError(w http.ResponseWriter, status int, message string) {
	writeJSONWithStatus(w, status, map[string]string{"error": message})
}

func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		next.ServeHTTP(w, r)
	})
}
