//window.onload = function() {
//  OnchangePackage();
//};

function OnchangePackage() {
        console.log(document.getElementById('package_id').value)

        $.ajax({
         type: 'POST',
         url: '/return_package_details',
         data: {package_id: document.getElementById('package_id').value, start_date: document.getElementById('start_date').value},
         dataType: 'json',
         success: function (response) {
                           document.getElementById("price").value = response.price;
                           document.getElementById("end_date").value = response.end_date;
                        },
        failure: function (response) {
            alert("failure")
        }
    });
}
//$("#delete_student").click(function(){
//    $.ajax({
//      type: 'POST',
//      url: "/_delete_student",
//      data: {student_id: 1},
//      dataType: "text",
//      success: function(data){
//                 alert("Deleted Student ID "+ student_id.toString());
//               }
//    });
//});