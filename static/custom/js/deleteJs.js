function deleteUser(id) {
    let status = confirm("Are you sure that you want to delete this record ?");
    if (status === true){
        $.ajax({
            type : 'POST',
            url : "/delete_user",
            contentType: 'application/json;',
            data : JSON.stringify(id)
        });
    }
}

function deleteCountry(id) {
    let status = confirm("Are you sure that you want to delete this record ?");
    if (status === true){
        $.ajax({
            type : 'POST',
            url : "/delete_country",
            contentType: 'application/json;',
            data : JSON.stringify(id)
        });
    }
}