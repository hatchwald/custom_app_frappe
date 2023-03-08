import sortBy from 'lodash.sortby';
frappe.listview_settings['posts'] = {
    refresh(listview){
        console.log("some")
        console.log(listview.sort_by)
        let datas = listview.data
        console.log(datas)
        const asc_datas = sortBy(datas,"title")
        console.log(asc_datas);
        // datas.sort((a,b) => {
        //     let x = a.title
        //     let y = b.title

        //     if (x < y) {
        //         return -1
        //     }
        //     if (x > y){
        //         return 1
        //     }
        //     return 0
        //     // let num = 0
        //     // switch (listview.sort_order) {
        //     //     case 'asc':
        //     //         num = 1
        //     //         break;
        //     //     case 'desc':
        //     //         num = -1
        //     //         break;
        //     //     default:
        //     //         num = 0
        //     //         break;
        //     // }
        //     // return num
           
        // })
        // listview.set_value(listview.data,datas)
    }
}