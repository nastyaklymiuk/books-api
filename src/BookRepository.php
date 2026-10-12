<?php
declare(strict_types=1);

namespace App;

final class BookRepository
{
    private array $books;

    public function __construct(string $file)
    {
        $json = file_get_contents($file);
        $this->books = json_decode($json, true, 512, JSON_THROW_ON_ERROR);
    }

    public function all(?string $genre = null, ?string $q = null): array
    {
        $result = array_filter($this->books, function (array $book) use ($genre, $q) {
            if ($genre && mb_strtolower($book['genre']) !== mb_strtolower($genre)) {
                return false;
            }
            if ($q) {
                $haystack = mb_strtolower($book['title'] . ' ' . $book['author']);
                if (!str_contains($haystack, mb_strtolower($q))) {
                    return false;
                }
            }
            return true;
        });

        return array_values($result);
    }

    public function find(int $id): ?array
    {
        foreach ($this->books as $book) {
            if ($book['id'] === $id) {
                return $book;
            }
        }
        return null;
    }

    public function genres(): array
    {
        return array_values(array_unique(array_column($this->books, 'genre')));
    }
}