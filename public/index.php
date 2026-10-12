<?php
declare(strict_types=1);

require __DIR__ . '/../vendor/autoload.php';

use App\BookRepository;

header('Content-Type: application/json; charset=utf-8');

function respond(int $code, array $data): never
{
    http_response_code($code);
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    respond(405, ['error' => 'Дозволено лише GET']);
}

$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$repo = new BookRepository(__DIR__ . '/../data/books.json');

if ($path === '/api/books') {
    $books = $repo->all($_GET['genre'] ?? null, $_GET['q'] ?? null);
    respond(200, ['count' => count($books), 'data' => $books]);
}

if (preg_match('#^/api/books/(\d+)$#', $path, $m)) {
    $book = $repo->find((int)$m[1]);
    $book ? respond(200, ['data' => $book])
          : respond(404, ['error' => 'Книгу не знайдено']);
}

if ($path === '/api/genres') {
    respond(200, ['data' => $repo->genres()]);
}

respond(404, ['error' => 'Невідомий маршрут']);