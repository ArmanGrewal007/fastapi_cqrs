API_URL="http://127.0.0.1:8000/users/"

echo "Adding users..."
curl -X POST "$API_URL" -H "Content-Type: application/json" -d '{"name": "Alice", "email": "alice@example.com"}'
curl -X POST "$API_URL" -H "Content-Type: application/json" -d '{"name": "Bob", "email": "bob@example.com"}'
curl -X POST "$API_URL" -H "Content-Type: application/json" -d '{"name": "Charlie", "email": "charlie@example.com"}'
curl -X POST "$API_URL" -H "Content-Type: application/json" -d '{"name": "David", "email": "david@example.com"}'
curl -X POST "$API_URL" -H "Content-Type: application/json" -d '{"name": "Eve", "email": "eve@example.com"}'

echo "✅ Users added successfully!"