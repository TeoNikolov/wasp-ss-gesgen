function startup() {
    getStyles()
        .then((styles) => {
            populateStyleSelector(styles);
        });
}

startup();
