function populateStyleSelector(styles) {
    const selectElement = document.getElementById('style-selector');
    selectElement.innerHTML = '';
    styles.forEach(style => {
        const option = document.createElement('option');
        option.text = style;
        selectElement.add(option);
    })
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
