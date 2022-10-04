#!/usr/bin/python3
"""
STOCK managment
"""
from dis import Instruction
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import Screen, ScreenManager
from datetime import datetime
from kivymd.app import MDApp
#from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.button import MDFloatingActionButton, MDRectangleFlatIconButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.list import TwoLineAvatarListItem
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivy.metrics import dp
from kivy.core.window import Window
import os
import database
import openpyxl

# comment this out before pushing
Window.size = (325, 580)
class Tab(MDFloatLayout, MDTabsBase):
	"""
	Tab class
	"""
	pass

class New_customer_layout(MDBoxLayout):
	"""
	PopUp window to add new customer
	"""
	def __init__(self) -> None:
		super(New_customer_layout, self).__init__()

	def addNewCustomer(self):
		"""
		When Add button pressed in the new customer dialog
		"""
		if self.customer_name.text and self.customer_tin_number.text and self.customer_region.text and self.customer_sub_city.text and self.customer_wereda.text and self.customer_phone_number.text and self.customer_account_created_date.text and self.customer_frequency_of_purchase.text and self.customer_total_purchase.text and self.customer_bank_account_number.text:
			#print(self.customer_bank_account_number.text)
			database.insertCustomer(self.customer_name.text,  self.customer_tin_number.text, self.customer_region.text, self.customer_sub_city.text, self.customer_wereda.text, self.customer_phone_number.text, self.customer_account_created_date.text, self.customer_frequency_of_purchase.text, self.customer_total_purchase.text, self.customer_bank_account_number.text)
			print('now you can close the popUp msg')
		else:
			print('fill all info msg')

class customerItem(TwoLineAvatarListItem):
	pass


class Store_window(MDScreen):
	"""
	store window class
	"""
	def __init__(self, **kwargs):
		super(Store_window, self).__init__(**kwargs)
		self.manager_open = False
		self.file_manager = MDFileManager(
			exit_manager=self.exit_manager,
			select_path=self.select_path,
			#previous=True,
		)
	

	def select_path(self, path):
		'''
        It will be called when you click on the file name
        or the catalog selection button.
        '''
		self.exit_manager()
		# this is for the customer table
		name, xtension = os.path.splitext(path)
		if xtension == '.xlsx':
			path = path
			wb_obj = openpyxl.load_workbook(path)
			sheet_obj = wb_obj.active
			row = sheet_obj.max_row
			column = sheet_obj.max_column
			customerFileList=[]
			for i in range (2, row+1):
				tempoTuple = []
				for j in range(1, column+1):
					cell_obj = sheet_obj.cell(row=i, column=j)
					tempoTuple.append(cell_obj.value)
				customerFileList.append(tempoTuple)
			for x in customerFileList:
				for a in x:
					if type(a) == datetime:
						x.insert(6, a.strftime("%d/%m/%y"))
						x.pop(7)
			for customerFi in customerFileList:
				database.insertCustomer(customerFi[0], customerFi[1], customerFi[2], customerFi[3], customerFi[4], customerFi[5], customerFi[6], customerFi[7], customerFi[8], customerFi[9])
			toast("Data recorded successfully")
		else: 
			"""
			msg that says invalid extnsion only xlsx accpeted
			"""
			toast("Invalid file type only (.xlsx) type accepted")

	def exit_manager(self, *args):
		'''
		Called when the user reaches the root of the directory tree
		'''
		self.manager_open = False
		self.file_manager.close()

	def on_enter(self):
		"""
		Entering window
		"""
		customersList = database.readSCustomer()
		itemList = database.readSItem()
		self.customer_tables = MDDataTable(
			pos_hint={'center_x': 0.5},
			size_hint=(1, 1),
			use_pagination=True,
			elevation=3,
			rows_num=50,
			column_data=[
				("ID", dp(15)),
				("Company Name", dp(30), ),
		        ("Phone Number", dp(30)),
		        ("Tin Number", dp(30)),
		        ("Bank Account", dp(30)),],
			row_data = customersList)
		self.customer_tables.bind(on_row_press=self.row_selected)
		newCustomerFile = MDFloatingActionButton(
			icon="attachment",
			pos_hint={'x': .91, 'y': .08},
			on_release=self.uploadCustomerFromFile
		)
		newCustomer = MDRectangleFlatIconButton(
			text="New",
			icon="plus",
			pos_hint={'x':.02, 'y': .05},
			on_release=self.newCustomer
			)
		self.customers_tab.add_widget(self.customer_tables)
		self.customers_tab.add_widget(newCustomer)
		self.customers_tab.add_widget(newCustomerFile)

		# for stock tab
		stock_tables = MDDataTable(
			pos_hint={'center_x': 0.5},
			size_hint=(1, 1),
			use_pagination=True,
			elevation=3,
			rows_num=50,
			column_data=[
				("ID", dp(15)),
				("Item Name", dp(30), ),
		        ("Item Quantity", dp(24)),
		        ("Purchased Price", dp(25)),
		        ("Selling Price Single", dp(32)),
				("Selling Price Bulk", dp(31))],
			row_data=itemList,)
		newStockFile = MDFloatingActionButton(
			icon="attachment",
			pos_hint={'x': .91, 'y': .08},
			on_release=self.uploadStockFromFile
		)
		newStock = MDRectangleFlatIconButton(
			text="New",
			icon="plus",
			pos_hint={'x':.02, 'y': .05},
			on_release=self.newStock
			)
		self.stock_tab.add_widget(stock_tables)
		self.stock_tab.add_widget(newStock)
		self.stock_tab.add_widget(newStockFile)
	def row_selected(self, table, row):
		start_index, end_index = row.table.recycle_data[row.index]['range']
		# this is to get the id since it is on the start_index
		print(row.table.recycle_data[start_index]["text"])
		self.customer_detail(row.table.recycle_data[start_index]["text"])

	def customer_detail(self, cId):
		customer=database.deatilCustomer(cId)
		print(customer)
		self.customer_detailPopUP = MDDialog(
			title="Customer Detail",
			type="simple",
			items=[
				customerItem(text="Name", secondary_text=str(customer[1])),
				customerItem(text="Tin Number", secondary_text=str(customer[2])),
				customerItem(text="Region", secondary_text=str(customer[3])),
				customerItem(text="Sub City", secondary_text=str(customer[4])),
				customerItem(text="Wereda", secondary_text=str(customer[5])),
				customerItem(text="Phone Number", secondary_text=str(customer[6])),
				customerItem(text="Account Created Date", secondary_text=str(customer[7])),
				customerItem(text="Frequency Of Purchase", secondary_text=str(customer[8])),
				customerItem(text="Total Purchase", secondary_text=str(customer[9])),
				customerItem(text="Bank Account", secondary_text=str(customer[10]))
			],
			buttons=[
				MDRaisedButton(
					text="Edit",
					on_press=self.editCustomer
				),
				MDRaisedButton(
					text="Delete",
					on_press=self.deleteCustomer
				)
			]
		)
		self.customer_detailPopUP.open()

	def editCustomer(self, inst):
		"""
		Edit Customer Information redirect to another popup where customer can be edited
		[OR] i am thinking like when the customerItem list is touched to promote to
		"""
		self.customer_detailPopUP.dismiss()

	def deleteCustomer(self, inst):
		"""
		Promte Warnig that this Customer is going to be deleted then delete
		* make the customerDetailPopup background color to become RED
		and show warning
		"""

	def uploadCustomerFromFile(self, inst):
		"""
		to upload Customer data from XL file in specific format
		"""
		path = os.path.expanduser("~")
		self.file_manager.show(path)
		self.manager_open = True

	def newCustomer(self, inst):
		"""
		Adding new single customer to database
		"""
		self.dialogNewCustomer = MDDialog(
			title="New Customer",
			type="custom",
			auto_dismiss=False,
			content_cls=New_customer_layout(),
			buttons=[
				MDRaisedButton(
					text="Close",
					theme_text_color="Custom",
					on_press=self.closeNewCustomer
				),
			]
		)
		self.dialogNewCustomer.open()
	def closeNewCustomer(self, inst):
		"""
		close button in add new customer dialog
		"""
		self.customer_tables.update_row_data(inst, database.readSCustomer())
		self.dialogNewCustomer.dismiss()

	def uploadStockFromFile(self, inst):
		"""
		to upload Customer data from XL file in specific format
			# open files and when specific file selected
			# check file extension
			# then check the format of the XL then
			# then travers data for each row and save it to database
			# then when all rows data are saved(til that show progress bar for user Interface) update MDDataTable
		"""
		path = os.path.expanduser("~")
		self.file_manager.show(path)
		self.manager_open = True

	def newStock(self, inst):
		"""
		Adding new single customer to database
			# first make popup
			# then to qualify and cahnge values type
			# then to insert into database by calling module `database.insertCustomer`
			# then update the MDDataTable
		"""


class main(MDApp):
	"""
	main class
	"""
	currentTime = datetime.now()
	Hr = currentTime.hour

	def build(self, first=False):
		"""
		build method
		"""
		if self.Hr < 18:
			self.theme_cls.theme_style = "Light"
		else:
			self.theme_cls.theme_style = "Dark"			
		self.theme_cls.primary_palette = 'Blue'
		screen_manager = ScreenManager()
		screen_manager.add_widget(Builder.load_file("stock.kv"))
		return screen_manager
		

if __name__ == "__main__":
	main().run()
