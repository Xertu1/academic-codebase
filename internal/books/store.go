package books

import (
	"errors"
	"sort"
	"sync"
	"time"
)

// Book represents a book resource exposed by the API.
type Book struct {
	ID        int64     `json:"id"`
	Title     string    `json:"title"`
	Author    string    `json:"author"`
	CreatedAt time.Time `json:"created_at"`
}

// Store keeps books in memory. It is safe for concurrent use.
type Store struct {
	mu    sync.RWMutex
	seq   int64
	books map[int64]Book
}

// ErrNotFound indicates that a book does not exist in the store.
var ErrNotFound = errors.New("book not found")

// NewStore creates a new in-memory store instance.
func NewStore() *Store {
	return &Store{books: make(map[int64]Book)}
}

// List returns all stored books ordered by their identifier.
func (s *Store) List() []Book {
	s.mu.RLock()
	defer s.mu.RUnlock()

	if len(s.books) == 0 {
		return []Book{}
	}

	items := make([]Book, 0, len(s.books))
	for _, b := range s.books {
		items = append(items, b)
	}
	sort.Slice(items, func(i, j int) bool { return items[i].ID < items[j].ID })
	return items
}

// Create adds a new book to the store and returns the stored value.
func (s *Store) Create(title, author string) Book {
	s.mu.Lock()
	defer s.mu.Unlock()

	s.seq++
	now := time.Now().UTC()
	book := Book{ID: s.seq, Title: title, Author: author, CreatedAt: now}
	s.books[book.ID] = book
	return book
}

// Get returns a single book by its identifier.
func (s *Store) Get(id int64) (Book, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	book, ok := s.books[id]
	if !ok {
		return Book{}, ErrNotFound
	}
	return book, nil
}
