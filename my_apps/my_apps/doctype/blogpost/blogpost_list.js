frappe.listview_settings['BlogPost'] = {
    formatters: {
        thumbnail(val){
            return `<img src="${val}" width="30%">`
        }
    }
}