
frappe.listview_settings['posts'] = {
    onload(listview){
        // code
        console.log(listview)
    },
    refresh(listview){
        console.log(listview.sort_by)
        let datas = listview.data
        console.log(datas)
        datas.sort((a,b) => {
            let x = a[listview.sort_by]
            let y = b[listview.sort_by]

            if (x < y) {
                return  (listview.sort_order == "asc") ? -1 : 1
            }
            if (x > y){
                return (listview.sort_order == "asc") ? 1 : -1
            }
            return 0
           
        })
        listview.data = datas
        listview.render_list()
        console.log(listview)
    }
}