async function getStyles() {
    try {
        const response = await fetch('/styles');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching styles:', error);
    }
}
