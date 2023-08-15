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
    try {
        const response = await fetch(
            '/generate_bvh',
            {
                method: 'POST',
                body: form_data
            },
        );
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error requesting generation of BVH:', error);
    }
}

async function postVisualise(form_data) {
    try {
        const response = await fetch(
            '/visualise',
            {
                method: 'POST',
                body: form_data
            },
        );
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error visualising BVH + WAV:', error);
    }
}
