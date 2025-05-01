const orginColSelect = document.getElementById('origin-selection');
const textTransformation = document.getElementById('data-text-transformation')
const textFields = document.getElementById('text-fields');
const numberFields = document.getElementById('number-fields');
const concatFields = document.getElementById('concatenate-fields');
const replaceFields = document.getElementById('replace-fields');
const dbSelection = document.getElementById('db-selection');
const originDbFields = document.getElementById('origin-db-options');
const targetDbFields = document.getElementById('target-db-fields');


orginColSelect.addEventListener('change', function () {
    const selected = this.value;

    textFields.style.display = 'none';
    numberFields.style.display = 'none';

    if (selected === 'name'|| selected === "department") {
        textFields.style.display = 'block';
    } else if (selected === 'salary' || selected === 'hours') {
        numberFields.style.display = 'block';
    }
});

textTransformation.addEventListener('change', function (){
    const textSelection = this.value;

    concatFields.style.display = 'none';
    replaceFields.style.display = 'none';

    if(textSelection === 'replace'){
        replaceFields.style.display = 'block';
    } else if(textSelection === 'concatenate'){
        concatFields.style.display = 'block';
    }
});



dbSelection.addEventListener('change', function(){
    const dbSelected = this.value;

    originDbFields.style.display = 'none';
    targetDbFields.style.display = 'none';

    if(dbSelected == 'source-database'){
        originDbFields.style.display = 'block';
    } else if(dbSelected == 'target-database'){
        targetDbFields.style.display = 'block';
        textFields.style.display = 'none';
        numberFields.style.display = 'none';
        concatFields.style.display = 'none';
        replaceFields.style.display = 'none';
    }

})