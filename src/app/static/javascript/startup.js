function startup() {
    getStyles()
        .then((styles) => {
            populateStyleSelector(styles);
        });

    getPoses()
        .then((poses) => {
            populatePoseSelector(poses);
        });

    // add form listeners
    const form_gg = document.getElementById("form-gesgen");
    form_gg.addEventListener('submit', submitFormGesGen);
    const form_vis = document.getElementById("form-vis");
    form_vis.addEventListener('submit', submitFormVis);
    const form_fbx = document.getElementById("form-fbx");
    form_fbx.addEventListener('submit', submitFormFBX);

    // temperature inputs
    var temp_slider = document.getElementById('temp_range');
    var temp_numeric = document.getElementById('temp_numeric');
    temp_slider.addEventListener('input', function (e) { temp_numeric.value = e.target.value; });
    temp_numeric.addEventListener('input', function (e) { temp_slider.value = e.target.value; });
    temp_numeric.addEventListener('keypress', function(e) {return isNumberKey(e); })

    // seed number input
    var seed_numeric = document.getElementById('seed_numeric');
    seed_numeric.value = getRandomInt(seed_numeric.max)
    seed_numeric.addEventListener('keypress', function(e) {return isNumberKey(e); })
}

function disableFormButton(form) {
    form.submit.disabled = true;
}

function enableFormButton(form) {
    form.submit.disabled = false;
}

function submitFormGesGen(event) {
    event.preventDefault();
    const form_gg = document.getElementById("form-gesgen");
    const data = new FormData(form_gg);
    disableFormButton(form_gg);
    postGenerateBVH(data)
        .then((jobId) => {
            poll(() => {
                return getCheckJob(jobId);
            },
            (pollResult) => {
                exitCondition = !(pollResult["state"] == "SUCCESS" || pollResult["state"] == "FAILURE");
                console.log(pollResult);
                return exitCondition;
            }, 2000)
            .then((pollResult) => {
                if (pollResult["state"] == "SUCCESS") {
                    saveFile(getFiles(jobId));
                }
                enableFormButton(form_gg);
            });
        });
}

function submitFormVis(event) {
    event.preventDefault();
    const form_vis = document.getElementById("form-vis");
    const data = new FormData(form_vis);
    disableFormButton(form_vis);
    postVisualise(data)
        .then((jobId) => {
            poll(() => {
                return getCheckJob(jobId);
            },
            (pollResult) => {
                exitCondition = !(pollResult["state"] == "SUCCESS" || pollResult["state"] == "FAILURE");
                console.log(pollResult);
                return exitCondition;
            }, 2000)
            .then((pollResult) => {
                if (pollResult["state"] == "SUCCESS") {
                    saveFile(getFiles(jobId));
                }
                enableFormButton(form_vis);
            });
        });
}

function submitFormFBX(event) {
    event.preventDefault();
    const form_fbx = document.getElementById("form-fbx");
    const data = new FormData(form_fbx);
    disableFormButton(form_fbx);
    postExportFBX(data)
        .then((jobId) => {
            poll(() => {
                return getCheckJob(jobId);
            },
            (pollResult) => {
                exitCondition = !(pollResult["state"] == "SUCCESS" || pollResult["state"] == "FAILURE");
                console.log(pollResult);
                return exitCondition;
            }, 2000)
            .then((pollResult) => {
                if (pollResult["state"] == "SUCCESS") {
                    saveFile(getFiles(jobId));
                }
                enableFormButton(form_fbx);
            });
        });
}
