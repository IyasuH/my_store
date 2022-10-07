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
from kivymd.uix.button import MDFloatingActionButton, MDRectangleFlatIconButton, MDRaisedButton, MDIconButton
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
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCard
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock

class MDashCard(MDCard):
	"""
	cards on the dashboard
	"""
	focu_color = ListProperty([1, 1, 1])
	unfocu_color = ListProperty([1, 1, 1])
	text1 = StringProperty("")
	text2 = StringProperty("")
	text3 = StringProperty("")
	# Icon (arrow-top-right, arrow-bottom-right)
	updownIcon = StringProperty("")
	# range b/n 0-100
	cpbValue = NumericProperty(0)
	cpbBarColor = ListProperty([1, 1, 1])

class MDCustomCard(MDCard):
	"""
	Crads for Customers page
	"""
	customerName = StringProperty("")
	companyName = StringProperty("")
	customerTinNumber = StringProperty("")
	customerPhoneNumber = StringProperty("")
	totalPurchased = StringProperty(0)
	itemPurchased = ListProperty([])

class CircularProgressBar(AnchorLayout):
	bar_color = ListProperty([1, 1, 1])
	bar_width = NumericProperty(2.5)
	# where this value is the percent for the progress bar
	set_value = NumericProperty(0)
	text = StringProperty("0%")
	value = NumericProperty(0)
	counter = 0
	duration = NumericProperty(1.5)

	def __init__(self, **kwargs):
		super(CircularProgressBar, self).__init__(**kwargs)
		Clock.schedule_once(self.animate, 0)

	def animate(self, *args):
		Clock.schedule_interval(self.percent_counter, self.duration/self.value)

	def percent_counter(self, *args):
		if self.counter < self.value:
			self.counter += 1 
			self.text = f"+{self.counter}%"
			self.set_value = self.counter
		else:
			Clock.unschedule(self.percent_counter)

# comment this out before deploying
Window.size = (327, 580)
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
		if self.customer_name.text and self.company_name.text and self.customer_tin_number.text and self.customer_city.text and self.customer_phone_number.text and self.customer_account_created_date.text and self.customer_frequency_of_purchase.text and self.customer_total_purchase.text and self.customer_bank_account_number.text:
			#print(self.customer_bank_account_number.text)
			database.insertCustomer(self.customer_name.text, self.company_name.text, self.customer_tin_number.text, self.customer_city.text, self.customer_phone_number.text, self.customer_account_created_date.text, self.customer_frequency_of_purchase.text, self.customer_total_purchase.text, self.customer_bank_account_number.text)
			toast('now you can close the popUp msg')
		else:
			toast('fill all info msg')

class New_stock_layout(MDBoxLayout):
	"""
	Popup to add new item
	"""
	def __init__(self) -> None:
		super(New_stock_layout, self).__init__()

	def addNewItem(self):
		"""
		when new item is added
		"""
		print("new stoklayout")
		print(self.item_name.text, self.item_quantity.text, self.purchased_price.text, self.purchased_date.text, self.selling_price_single.text, self.selling_price_bulk.text)
		if self.item_name.text and self.item_quantity.text and self.purchased_price.text and self.purchased_date.text and self.selling_price_single.text and self.selling_price_bulk.text:
			database.insertItem(self.item_name.text, self.item_quantity.text, self.purchased_price.text, self.purchased_date.text, self.selling_price_single.text, self.selling_price_bulk.text)
			toast('Data saved successfully now you can close')
		else:
			toast('Complete filling the info')

class customerItem(TwoLineAvatarListItem):
	pass

class Detail_item_layout(MDBoxLayout):
	def __init__(self, Id) -> None:
		super(Detail_item_layout, self).__init__()
		print(Id)
		self.stock = database.detailItem(Id)
		self.item_name.secondary_text = str(self.stock[1])
		self.item_quantity.secondary_text = str(self.stock[2])
		self.purchased_price.secondary_text = str(self.stock[3])
		self.purchased_date.secondary_text = str(self.stock[4])
		self.single_selling_price.secondary_text = str(self.stock[5])
		self.bulk_selling_price.secondary_text = str(self.stock[6])
		self.updated_at.secondary_text = str(self.stock[7])

class Home(MDScreen):
	"""
	main home page
	"""
	#class Stock(MDScreen):
		#"""
		#Stock page
		#"""
	def __init__(self, **kwargs):
		super(Home, self).__init__(**kwargs)
		self.manager_open = False
		self.item_manager = MDFileManager(
			exit_manager=self.exit_manager,
			select_path=self.select_item_path,
		)
	def select_item_path(self, path):
		'''
		It will be called when you click on the file name
		or the catalog selection button.
		'''
		self.exit_manager()
		# this is for the customer table
		name, xtension = os.path.splitext(path)
		if xtension == '.xlsx':
			simplepath = path
			wb_obj = openpyxl.load_workbook(path)
			sheet_obj = wb_obj.active
			row = sheet_obj.max_row
			column = sheet_obj.max_column
			itemFileList=[]
			for i in range (2, row+1):
				tempoTuple = []
				for j in range(1, column+1):
					cell_obj = sheet_obj.cell(row=i, column=j)
					tempoTuple.append(cell_obj.value)
				itemFileList.append(tempoTuple)
			# here what i done is to change datetime type to str
			# since when uploaded from XL it is datetime type
			for x in itemFileList:
				for a in x:
					if type(a) == datetime:
						x.insert(6, a.strftime("%d/%m/%y"))
						x.pop(7)
			for itemFi in itemFileList:
				database.insertCustomer(itemFi[0], itemFi[1], itemFi[2], itemFi[3], itemFi[4], itemFi[5])
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
		self.item_manager.close()			
	def stockFunc(self):
		"""
		This function is to return the items table
		"""
		self.itemList = database.readSItem()
		for x in self.itemList:
			if x[2] <= 0:
				availability = ("alert-circle", [1, 0, 0, 1], "No item")			
			elif x[2] < 10:
				availability = ("alert", [255/256, 165/256, 0, 1], "less than 10")
			else:
				availability = ("checkbox-marked-circle", [39/256, 174/256, 96/256, 1], "Available")
			x.insert(2, availability)

		self.stock_tables = MDDataTable(
			pos_hint={'center_x': 0.5},
			size_hint=(1, 1),
			rows_num=100,
			#use_pagination=False,
			#background_color_header=main().theme_cls.bg_darkest,
			#background_color_cell=main().theme_cls.bg_dark,
			#background_color=main().theme_cls.bg_darkest,
			elevation=3,
			#rows_num=50,
			column_data=[
				("ID", dp(7)),
				("Name", dp(14)),
				("Availability", dp(22)),
				("Qty", dp(10)),
				("P_Price", dp(13)),
				("S-Price", dp(13)),
				("B-Price", dp(13))],
			row_data=self.itemList,)
		self.stock_tables.bind(on_row_press=self.item_row_selected)
		newStockFile = MDIconButton(
			icon="attachment",
			pos_hint={'x': .8, 'y': .05},
			theme_icon_color="Custom",
			icon_color='white',
			md_bg_color='blue',
			#set_radius=[50,50,50,50],
			#rounded_button = True,
			on_release=self.uploadStockFromFile
		)				
		newStock = MDRaisedButton(
			text="New",
			icon="plus",
			pos_hint={'x':.02, 'y': .03},
			on_release=self.newStock
			)
		self.tock_tab.add_widget(self.stock_tables)
		self.tock_tab.add_widget(newStock)
		self.tock_tab.add_widget(newStockFile)

	def item_row_selected(self, table, row):
		"""
		When row selected
		"""
		start_index, end_index = row.table.recycle_data[row.index]['range']
		# this is to get the id since it is on the start_index
		self.item_detail(row.table.recycle_data[start_index]["text"])

	def item_detail(self, Id):
		"""
		dialog popup to display item detail
		"""
		#item = database.detailItem(Id)
		self.item_detailPopup = MDDialog(
			title="Item detail",
			type="custom",
			content_cls=Detail_item_layout(Id),
			buttons=[
				MDRaisedButton(
					text="Edit",
					on_press=self.editStock,
				),
				MDRaisedButton(
					text="Delete"
				)
			]
		)
		self.item_detailPopup.open()

	def editStock(self, *args):
		print('Error: ', args[0])

	def uploadStockFromFile(self, inst):
		"""
		uploading stock data from XL file
		"""
		path = os.path.expanduser("~")
		self.item_manager.show(path)
		self.manager_open = True
	def newStock(self, inst):
		"""
		new individual stock
		"""
		self.dialogNewStock = MDDialog(
			title="New Item",
			type="custom",
			auto_dismiss=False,
			content_cls=New_stock_layout(),
			buttons=[
				MDRaisedButton(
					text="Close",
					theme_text_color="Custom",
					on_press=self.closeNewStock
				)
			]
		)
		self.dialogNewStock.open()
	def closeNewStock(self, inst):
		#self.stock_tables.update_row_data(inst, self.itemList)
		self.stockFunc()
		self.dialogNewStock.dismiss()

	def customerFunc(self):
		"""
		When customer tab selected
		"""
		self.customerTab.clear_widgets()
		customersList = database.readSCustomer()
		for x in customersList:
			self.customerTab.add_widget(MDCustomCard(
				customerName = x[1],
				companyName = x[2],
				customerTinNumber = str(x[5]),
				customerPhoneNumber = str(x[4]),
				totalPurchased = str(x[6]),
				#itemPurchased = database.read,
			))
			#self.customerTab.add_widget(customerCard)

	def newCustomer(self):
		"""
		Adding new single customer to database
		"""
		print('on new customers')
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
		self.dialogNewCustomer.dismiss()


class DashBoard(MDScreen):
	"""
	This page is going to contain general-over
		all informat expenseProfit using different cards
	"""

class Sales(MDScreen):
	"""
	Sales page
	"""
	pass

class CashFlow(MDScreen):
	"""
	Cash Flow pagecustomerItem
	"""
	pass

class Customer(MDScreen):
	"""
	Customer page
	"""
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
			self.theme_cls.theme_style = "Dark"
		else:
			self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = 'Blue'
		self.theme_cls.material_style ="M3"
		screen_manager = ScreenManager()
		#screen_manager.add_widget(Builder.load_file("stock.kv"))
		screen_manager.add_widget(Builder.load_file("home.kv"))
		return screen_manager
		

if __name__ == "__main__":
	main().run()
