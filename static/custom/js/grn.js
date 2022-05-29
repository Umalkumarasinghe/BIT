var dataModel = {
    grnData: {
        id: '',
        supplier_id: '',
        grn_order_name: '',
        grn_created_date: '',
        grn_expected_date: '',
        grn_state:''
    },
    itemData: [] // object array this will fill when added to table
}

var itemId = 0;

// Use isEdit flag to identify whether new addin or editing.
var isEdit = false;

// this will hold the editing item id when editing
var editingItemId = null;

function fillTable() {
    if (
        document.getElementById("item_product_id").value != "" ||
        document.getElementById("demand_quantity").value != "" ||
        document.getElementById("received_quantity").value != "" ||
        document.getElementById("remaining_quantity").value != ""
    ) {
        if (isEdit) {
            // selecting row to update values in the table. We use editingItemId value here set while in the editItem function.
            var currentEditingRow = document.querySelectorAll("[data-itemid='" + editingItemId + "']")[0]
            console.log(currentEditingRow);

            // item id is set to not editable so dont want to upadte it
            //currentEditingRow.children[0].innerHTML = document.getElementById("itemId").value

            var item_product_id = document.getElementById("item_product_id").value;
            var demand_quantity = document.getElementById("demand_quantity").value;
            var received_quantity = document.getElementById("received_quantity").value;
            var remaining_quantity = document.getElementById("remaining_quantity").value;
            console.log(document.getElementById("remaining_quantity").value);
            var item_product_id_element = document.getElementById("item_product_id");
            var subtotal_text = item_product_id_element.options[item_product_id_element.selectedIndex].innerHTML;
            // get new valued
            var new_item_product_id = document.getElementById("item_product_id").value;
            var new_demand_quantity = document.getElementById("demand_quantity").value;
            var new_received_quantity = document.getElementById("received_quantity").value;
            var new_remaining_quantity = document.getElementById("remaining_quantity").value;
            var new_item_product_id_element = document.getElementById("item_product_id");
            var new_subtotal_text = new_item_product_id_element.options[new_item_product_id_element.selectedIndex].innerHTML;
            ;
            // update rate,qty in table
            currentEditingRow.children[0].innerHTML = new_subtotal_text;
            currentEditingRow.children[1].innerHTML = new_demand_quantity;
            currentEditingRow.children[2].innerHTML = new_received_quantity;
            currentEditingRow.children[3].innerHTML = new_remaining_quantity;


            // update rate,qty in dataModel.itemData
            var item = dataModel.itemData.find(x => x.itemId == editingItemId);
            item.item_product_id = item_product_id;
            item.demand_quantity = demand_quantity;
            item.received_quantity = received_quantity;
            item.remaining_quantity = remaining_quantity;


            // reset editingItemId
            editingItemId = null;
            document.getElementById("btnItemForm").value = 'Add';

            //to confirm
            console.log(dataModel.itemData);

        }
        else {
            var table = document.getElementById("grnTable");
            // adding new row and cells
            var row = table.insertRow(-1);
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            var cell5 = row.insertCell(4);


            // Fetching Values
//            var itemId = document.getElementById("itemId").value;
            var item_product_id = document.getElementById("item_product_id").value;
            var demand_quantity = document.getElementById("demand_quantity").value;
            var received_quantity = document.getElementById("received_quantity").value;
            var remaining_quantity = document.getElementById("remaining_quantity").value;
            var item_product_id_element = document.getElementById("item_product_id");
            var subtotal_text = item_product_id_element.options[item_product_id_element.selectedIndex].innerHTML;


            //Setting Values
//            cell1.innerHTML = itemId;
            cell1.innerHTML = subtotal_text;
            cell2.innerHTML = demand_quantity;
            cell3.innerHTML = received_quantity;
            cell4.innerHTML = remaining_quantity;

            // For action buttons data attribute are used to pass the id of the item for deletion and edition.

            cell5.innerHTML = "<button type='button' class='btn btn-dark btn-sm mr-2' onclick='editItem(this)' data-itemid=" + itemId +  " data-item_product_id=" + item_product_id + "><span class='fa fa-edit'></span></button>" +
                "<button type='button' class='btn btn-danger btn-sm' onclick='deleteRow(this)' data-itemid=" + itemId + "><span class='fa fa-trash'></span></button>";

            // set item id to data attribute of the row. thi will need in edit and remove. inspect the tr element and this will be attribute called "data-itemid".
            row.dataset.itemid = itemId;

            // Add new data to model
            addToModel({ itemId, item_product_id, demand_quantity, received_quantity, remaining_quantity });
            itemId++;
        }


        // reset isEdit and enable Item id field
        this.isEdit = false;
//        document.getElementById("itemId").disabled = false;

        // Clear values in fields after adding/Editing

        document.getElementById("demand_quantity").value = '';
        document.getElementById("received_quantity").value = '';
        document.getElementById("remaining_quantity").value = '';

    }
}

function deleteRow(row) {
    deletingItemId = row.dataset.itemid;
    // console.log(deletingItemId);
    var currentDeletingRow = document.querySelectorAll("[data-itemid='" + deletingItemId + "']")[0];
    currentDeletingRow.remove();

    // find item and index of item to be removed
    var itemTobeRemoved = dataModel.itemData.find(x => x.itemId == deletingItemId)
    var indexTobeRemoved = dataModel.itemData.indexOf(itemTobeRemoved);

    // console.log(indexTobeRemoved);
    // console.log(dataModel.itemData);
    // Array.splice method removes the element at passed index, 1 is to remove one element from that index.
    dataModel.itemData.splice(indexTobeRemoved, 1)

    //console.log(dataModel.itemData);

}

function addToModel(newItem) {
console.log(newItem);
    dataModel.itemData.push(newItem);
//    debugger;
    console.log(dataModel);
}

function editItem(Obj) {
    this.isEdit = true;

    // get item ID from data attribute and set it to global var editingItemId.
    console.log(dataModel);
    editItemId = Obj.dataset.itemid;
    console.log(editItemId);
    editingItemId = editItemId;
    console.log(dataModel);

    // find item from itemData array and populate values in from
    var item = dataModel.itemData.find(x => x.itemId == editItemId);
    console.log(item)

    // here item id field is disbaled. not allowing to edit item id but showing id. if edited it will effect edit and remove functionalities.
//    document.getElementById("itemId").disabled = true;
//    document.getElementById("itemId").value = item.itemId;

    // set other values
    document.getElementById("item_product_id").value = item.item_product_id;
    document.getElementById("demand_quantity").value = item.demand_quantity;
    document.getElementById("received_quantity").value = item.received_quantity;
    document.getElementById("remaining_quantity").value = item.remaining_quantity;
    document.getElementById("remaining_quantity").max = item.remaining_quantity;

    //set button text to edit
    document.getElementById("btnItemForm").value = 'Update';
}

function submitAll(){
    // set order details
    dataModel.purchase_orderData.supplier_id =  document.getElementById("supplier_id").value
    dataModel.purchase_orderData.name =  document.getElementById("purchase_order_name").value
    dataModel.purchase_orderData.purchase_order_created_date =  document.getElementById("purchase_order_created_date").value
    dataModel.purchase_orderData.purchase_order_expected_date =  document.getElementById("purchase_order_expected_date").value
    dataModel.purchase_orderData.purchase_total =  document.getElementById("purchase_total").value

    // items in the table already set now,

    // here we can handle the final data object. HTTP request or any other way to send bak end
    // this is a console.log just to confirm

    console.log('FINAL OBJECT', dataModel);
    console.log(JSON.stringify(dataModel));
    $.ajax({
         type: 'POST',
         url: '/create_purchase_order',
         data: { 'values' : JSON.stringify(dataModel) } ,
         dataType: 'json',
         success: function (response) {
                           document.getElementById("price").value = response.price;
                           document.getElementById("purchase_order_expected_date").value = response.purchase_order_expected_date;
                        },
        failure: function (response) {
            alert("failure")
        }
    });
}

function createGrn(){
    // set order details
    dataModel.purchase_orderData.supplier_id =  document.getElementById("supplier_id").value
    dataModel.purchase_orderData.name =  document.getElementById("purchase_order_name").value
    dataModel.purchase_orderData.purchase_order_created_date =  document.getElementById("purchase_order_created_date").value
    dataModel.purchase_orderData.purchase_order_expected_date =  document.getElementById("purchase_order_expected_date").value
    dataModel.purchase_orderData.purchase_total =  document.getElementById("purchase_total").value

    // items in the table already set now,

    // here we can handle the final data object. HTTP request or any other way to send bak end
    // this is a console.log just to confirm

    console.log('FINAL OBJECT', dataModel);
    console.log(JSON.stringify(dataModel));
    $.ajax({
         type: 'POST',
         url: '/create_grn',
         data: { 'values' : JSON.stringify(dataModel) } ,
         dataType: 'json',
         success: function (response) {
                           window.location.href = "/view_purchase_order";
        },
        failure: function (response) {
            window.location.href = "/view_purchase_order";
        }
    });
}

function updateAll(){
    // set order details
    dataModel.grnData.supplier_id =  document.getElementById("supplier_id").value
    dataModel.grnData.grn_order_name =  document.getElementById("grn_name").value
    dataModel.grnData.grn_created_date =  document.getElementById("grn_created_date").value
    dataModel.grnData.grn_expected_date =  document.getElementById("grn_expected_date").value
    dataModel.grnData.grn_state =  document.getElementById("grn_state").value

    // items in the table already set now,

    // here we can handle the final data object. HTTP request or any other way to send back end
    // this is a console.log just to confirm

    console.log('FINAL OBJECT', dataModel);
    console.log(JSON.stringify(dataModel));
    $.ajax({
         type: 'POST',
         url: '/edit_grn',
         data: { 'values' : JSON.stringify(dataModel) } ,
         dataType: 'json',
         success: function (response) {
                           window.location.reload();
        },
        failure: function (response) {
            window.location.reload();
            debugger;
        }
    });
}

function completeGRN() {
    console.log(document.getElementById('id').value)
    $.ajax({
    type: 'POST',
    url: '/complete_grn',
    data: {grn_id: document.getElementById('id').value},
    dataType: 'json',
    success: function (response) {
        window.location.href = "/edit_grn_view?id=" + response.id;
        alert("Successfully Completed")
    },
    failure: function (response) {
        window.location.href = "/view_purchase_order";
    }
    });
}

function calculateTotal(){
    let unit_price = document.getElementById('unit_price').value;
    let quantity = document.getElementById('quantity').value;
    document.getElementById('subtotal').value = unit_price * quantity
}

function OnchangeProduct() {
    console.log(document.getElementById('item_product_id').value)
        $.ajax({
        type: 'POST',
        url: '/get_unit_price',
        data: {item_product_id: document.getElementById('item_product_id').value},
        dataType: 'json',
        success: function (response) {
           document.getElementById("unit_price").value = response.price;
        },
    failure: function (response) {
        alert("failure")
    }
    });
}