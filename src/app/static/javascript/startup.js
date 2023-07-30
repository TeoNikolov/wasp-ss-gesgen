function startup() {
    getStyles()
        .then((styles) => {
            populateStyleSelector(styles);
        });

    // add form listeners
    const form_gg = document.getElementById("form-gesgen");
    form_gg.addEventListener('submit', submitFormGesGen);

    // temperature inputs
    var temp_slider = document.getElementById('temp_range');
    var temp_numeric = document.getElementById('temp_numeric');
    temp_slider.addEventListener('input', function (e) { temp_numeric.value = e.target.value; });
    temp_numeric.addEventListener('input', function (e) { temp_slider.value = e.target.value; });
    temp_numeric.addEventListener('keypress', function(e) {return isNumberKey(e); })

    // seed number input
    var seed_numeric = document.getElementById('seed_numeric');
    console.log(seed_numeric.max)
    seed_numeric.value = getRandomInt(seed_numeric.max)
    seed_numeric.addEventListener('keypress', function(e) {return isNumberKey(e); })
}

function submitFormGesGen(event) {
    event.preventDefault();
    const form_gg = document.getElementById("form-gesgen");
    const data = new FormData(form_gg);
    postGenerateBVH(data);
}

startup();
