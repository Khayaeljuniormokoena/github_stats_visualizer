export async function fetchData() {
    const response = await fetch('http://localhost:5000/api/repos/username');
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
}
