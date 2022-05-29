function OnchangeNic(nic_no) {
    let nic_number;
    if (nic_no){
        nic_number = nic_no.replace(/\s/g, '');
        if (nic_number.length === 10){
            if (nic_number.match(/\d{9}(X|V|x|v)/g) != null){
                let year = parseInt(nic_number.substring(0, 2)) + 1900;
                let days = parseInt(nic_number.substring(2, 5));
                GetValues(year, days)
            }
            else{
                alert("Invalid NIC")
            }
        }
        else {
            if (nic_number.length === 12){
                if (nic_number.match(/\d{12}/g) != null){
                    let year = parseInt(nic_number.substring(0, 4));
                    let days = parseInt(nic_number.substring(4, 7));
                    GetValues(year, days)
                }
            }
            else {
                alert("Invalid NIC")
            }
        }
    }
    else {
        alert("Invalid NIC")
    }
}

function GetValues(year, days){
    let actual_days;
    let month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    let month = 0;
    if (days >= 501 && days <= 866 || days >= 1 && days <= 366){
        if (days >= 501 && days <= 866){
            actual_days = days - 500;
        }
        else {
            actual_days = days;
        }

        for (i=0; i < month_days.length; i++){
            month += 1;
            if (actual_days <= month_days[i]){
                break
            }
            else{
                actual_days -= month_days[i];
            }
        }
        if (days < 500){
            gender = 'male'
        }
        else {
            gender = 'female'
        }

        document.getElementById('date_of_birth').value = year + '-' + month.toString().padStart(2, '0') + '-' + actual_days.toString().padStart(2, '0');
        document.getElementById('age').value = new Date().getFullYear() - year;
        document.getElementById(gender).checked = true;
    }
    else{
        alert("Invalid NIC")
    }
}

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