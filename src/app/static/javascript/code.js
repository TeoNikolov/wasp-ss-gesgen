function populateStyleSelector(styles) {
    const selectElement = document.getElementById('style-selector');
    selectElement.innerHTML = '';
    styles.forEach(style => {
        const option = document.createElement('option');
        option.text = style;
        selectElement.add(option);
    })
}
