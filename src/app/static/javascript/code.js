function populateStyleSelector(styles) {
    const selectElement = document.getElementById('style-selector');
    selectElement.innerHTML = '';
    styles.sort();
    styles.forEach(style => {
        const option = document.createElement('option');
        option.text = style;
        selectElement.add(option);
    })
}

function populatePoseSelector(poses) {
    const selectElement = document.getElementById('pose-selector');
    selectElement.innerHTML = '';
    poses.sort((a, b) => parseInt(a.replace('pose_', ''), 10) - parseInt(b.replace('pose_', ''), 10));
    poses.forEach(style => {
        const option = document.createElement('option');
        option.text = style;
        selectElement.add(option);
    })
}

function displayPoseImage(imageUrl) {
    const imageElement = document.getElementById('pose-image');
    imageElement.src = imageUrl;
    imageElement.style.display = 'inline';
}

function isNumberKey(event) {
    var charCode = (event.which) ? event.which : event.keyCode
    if (charCode > 31 && (charCode < 48 || charCode > 57))
      return false;
    return true;
}

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

const poll = async function (fn, fnCondition, ms) {
    let result = await fn();
        while (fnCondition(result)) {
            await wait(ms);
            result = await fn();
        }
    return result;
};

const wait = function (ms = 1000) {
    return new Promise(resolve => {
        setTimeout(resolve, ms);
    });
};

function saveFile(responsePromise) {
    let filename = 'unknown_filename';

    responsePromise
    .then((response) => {
        const CDHeader = response.headers.get("Content-Disposition");
        filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
        var matches = filenameRegex.exec(CDHeader);
        if (matches != null && matches[1]) {
            filename = matches[1].replace(/['"]/g, '');
        }
        return response.blob();
    })
    .then((blob) => URL.createObjectURL(blob))
    .then(url => {
        var a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
        a.click();
        a.remove();  //afterwards we remove the element again
        URL.revokeObjectURL(url);
    });
}
