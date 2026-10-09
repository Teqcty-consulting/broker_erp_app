import frappe


def before_install():
	"""Remove Module Defs left behind by an earlier, failed install of this app.

	Frappe inserts the app's Module Defs early in install_app and only marks the
	app installed at the very end, so an install that fails in between leaves a
	"Broker" Module Def on a site where broker_app is not installed. The next
	install (directly, or as broker_pwa's required app) then stops with
	"Duplicate entry 'Broker' for key 'PRIMARY'". This hook runs before the
	Module Defs are inserted; at that point any row owned by broker_app can only
	be such a leftover. Rows owned by other apps are left alone."""
	for module in frappe.get_module_list("broker_app"):
		if frappe.db.get_value("Module Def", module, "app_name") == "broker_app":
			frappe.db.delete("Module Def", {"name": module})
