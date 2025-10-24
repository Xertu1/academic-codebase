package server_test

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"academic-codebase/goapi/internal/books"
	"academic-codebase/goapi/internal/server"
)

func newTestHandler() http.Handler {
	store := books.NewStore()
	srv := server.New(store)
	return srv.Routes()
}

func TestHealth(t *testing.T) {
	handler := newTestHandler()
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	resp := httptest.NewRecorder()

	handler.ServeHTTP(resp, req)

	if resp.Code != http.StatusOK {
		t.Fatalf("expected status %d, got %d", http.StatusOK, resp.Code)
	}

	var body map[string]string
	if err := json.NewDecoder(resp.Body).Decode(&body); err != nil {
		t.Fatalf("decode response: %v", err)
	}

	if body["status"] != "ok" {
		t.Fatalf("unexpected health response: %v", body)
	}
}

func TestCreateAndListBooks(t *testing.T) {
	store := books.NewStore()
	srv := server.New(store)
	handler := srv.Routes()

	payload := map[string]string{"title": "The Go Programming Language", "author": "Alan A. A. Donovan"}
	buf, _ := json.Marshal(payload)
	req := httptest.NewRequest(http.MethodPost, "/books", bytes.NewReader(buf))
	resp := httptest.NewRecorder()

	handler.ServeHTTP(resp, req)

	if resp.Code != http.StatusCreated {
		t.Fatalf("expected status %d, got %d", http.StatusCreated, resp.Code)
	}

	var created books.Book
	if err := json.NewDecoder(resp.Body).Decode(&created); err != nil {
		t.Fatalf("decode create response: %v", err)
	}

	if created.ID == 0 {
		t.Fatalf("expected non-zero id")
	}

	listReq := httptest.NewRequest(http.MethodGet, "/books", nil)
	listResp := httptest.NewRecorder()
	handler.ServeHTTP(listResp, listReq)

	if listResp.Code != http.StatusOK {
		t.Fatalf("expected status %d, got %d", http.StatusOK, listResp.Code)
	}

	var listed struct {
		Items []books.Book `json:"items"`
	}
	if err := json.NewDecoder(listResp.Body).Decode(&listed); err != nil {
		t.Fatalf("decode list response: %v", err)
	}

	if len(listed.Items) != 1 {
		t.Fatalf("expected 1 book, got %d", len(listed.Items))
	}

	if listed.Items[0].Title != payload["title"] {
		t.Fatalf("unexpected title: %s", listed.Items[0].Title)
	}
}

func TestGetBookByID(t *testing.T) {
	store := books.NewStore()
	srv := server.New(store)
	handler := srv.Routes()

	created := store.Create("Concurrency in Go", "Katherine Cox-Buday")

	req := httptest.NewRequest(http.MethodGet, "/books/1", nil)
	resp := httptest.NewRecorder()
	handler.ServeHTTP(resp, req)

	if resp.Code != http.StatusOK {
		t.Fatalf("expected status %d, got %d", http.StatusOK, resp.Code)
	}

	var got books.Book
	if err := json.NewDecoder(resp.Body).Decode(&got); err != nil {
		t.Fatalf("decode response: %v", err)
	}

	if got.ID != created.ID || got.Title != created.Title {
		t.Fatalf("unexpected book returned: %+v", got)
	}
}
