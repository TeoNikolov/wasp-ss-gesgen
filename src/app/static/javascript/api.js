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

async function getPoseImages(imageNames) {
    try {
        const imagePromises = imageNames.map(async (imageName) => {
            const response = await fetch(`/pose_images/${imageName}`);
            if (!response.ok) {
                throw new Error(`Failed to fetch image: ${imageName}`);
            }
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            return { imageName, url };
        });

        const images = await Promise.all(imagePromises);
        return images;
    } catch (error) {
        console.error('Error fetching images:', error);
        return [];
    }
}

async function getCheckJob(jobId) {
    try {
        const response = await fetch("/job_id/" + jobId);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching job status:', error);
    }
}

async function getFiles(jobId) {
    try {
        const response = await fetch("/get_files/" + jobId);
        const data = await response;
        return data;
    } catch (error) {
        console.error('Error fetching files:', error);
    }
}

async function postGenerateBVH(form_data) {
    const response = await fetch(
        '/generate_bvh',
        {
            method: 'POST',
            body: form_data
        },
    );
    const data = await response.json();
    if (!response.ok) {
        throw new Error(`Failed to generate BVH: ${data.detail}, ${response.status}`);
    }
    return data;
}

async function postVisualise(form_data) {
    const response = await fetch(
        '/visualise',
        {
            method: 'POST',
            body: form_data
        },
    );
    const data = await response.json();
    if (!response.ok) {
        throw new Error(`Failed to visualise MP4: ${data.detail}, ${response.status}`);
    }
    return data
}

async function postExportFBX(form_data) {
    const response = await fetch(
        '/export_fbx',
        {
            method: 'POST',
            body: form_data
        },
    );
    const data = await response.json();
    if (!response.ok) {
        throw new Error(`Failed to export FBX: ${data.detail}, ${response.status}`);
    }
    return data;
}
