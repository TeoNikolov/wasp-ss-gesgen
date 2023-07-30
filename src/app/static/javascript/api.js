async function getStyles() {
    try {
        const response = await fetch('/styles');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching styles:', error);
    }
}

async function getPoses() {
    try {
        const response = await fetch('/poses');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching styles:', error);
    }
}

async function postGenerateBVH(form_data) {
    try {
        const response = await fetch(
            '/generate_bvh',
            {
                method: 'POST',
                body: form_data
                // headers: {'content-type': 'multipart/form-data'}
            },
        );
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error requesting generation of BVH:', error);
    }
}
