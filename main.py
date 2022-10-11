#!/usr/bin/python3
"""
STOCK managment
"""
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import Screen, ScreenManager
from datetime import datetime
from datetime import date
from kivymd.app import MDApp
#from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.button import MDFloatingActionButton, MDRectangleFlatIconButton, MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.list import TwoLineAvatarListItem, ThreeLineAvatarIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivy.metrics import dp
from kivy.core.window import Window
import os
import database
import openpyxl
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCard, MDCardSwipe
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield.textfield import MDTextField

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

class MDXpense(MDCard):
	"""
	Single expense item card
	For now it is going only to have three values
		Item - Expense name
		Amount - Expense Amount
		Date - date where expense made
	"""
	expenseName = StringProperty("")
	expenseAmount = StringProperty("")
	expenseDate = StringProperty("")

class MDSalesCard(MDCard):
	"""
	Single sales item card
	For now it is going only to have three values
		Item - Sales Item Name
		Qty - Quantity
		amount - amount gained (qty*single value)value
		date - when sales made	
	"""
	salesName = StringProperty("")
	salesQty = StringProperty("")
	salesAmount = StringProperty("")
	salesDate = StringProperty("")


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
	"""
	Circular progressbar
	"""
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
Window.size = (327, 585)

class Bank_list_item(MDCardSwipe):
	"""
	Bank list items
	"""
	bankName = StringProperty("")
	bankAccountCreatedAt = StringProperty("")
	bankAmount = StringProperty("")
	bankId = NumericProperty(0)
	icon = StringProperty("")
	def __init__(self, *args, **kwargs):
		super(Bank_list_item, self).__init__(**kwargs)
	def deleteAccount(self, bankId):
		"""
		delete call method
		"""
		self.dialogDeleteBank = MDDialog(
			title="Are You Sure?",
			text="You won't be able to revert this!",
			#auto_dismiss=False,
			radius=[20, 7, 20, 7],
			buttons=[
				MDFlatButton(
					text="CANCEL",
					theme_text_color="Custom",
					on_press=self.cancleDeleteBank
				),
				MDRaisedButton(
					text="DELETE",
					theme_text_color="Custom",
					md_bg_color=(243/255, 63/255, 63/255, 1),
					on_release=self.sureDeleteBank
				)
			]
		)
		self.dialogDeleteBank.open()
	def cancleDeleteBank(self, *args):
		"""
		cancle deleting 
		"""
		self.dialogDeleteBank.dismiss()

	def sureDeleteBank(self, *args):
		"""
		do the delete
		"""
		print("deleted!!")
		self.dialogDeleteBank.dismiss()
		database.deleteBankAcc(self.bankId)
		toast("Your File Has been deleted.")
		self.dialogDeleteBank.dismiss()

	def editAccount(self, bankId):
		"""
		edit call method
		"""
		#Setting().dismissDialogB()
		"""
			Creates New dialogbox where bank elements
			described in the textfield
		"""
		self.dialogEditBank = MDDialog(
			title="Edit Bank info",
			type="custom",
			auto_dismiss=False,
			content_cls=Edit_Bank_layout(bankId),
			buttons=[
				MDRaisedButton(
					text="Close",
					theme_text_color="Custom",
					on_press=self.closeEditBank
				),
			]
		)
		self.dialogEditBank.open()

	def closeEditBank(self, *args):
		"""
		close edit bank
		"""
		print("close edit")
		self.dialogEditBank.dismiss()

class Bank_list_layout(MDBoxLayout):
	"""

	This class is for listsing bank accounts from database table
	"""
	def __init__(self) -> None:
		super(Bank_list_layout, self).__init__()
		banks = database.readBankAcc()
		self.bank_mdlist.clear_widgets()
		for bank in banks:
			self.bank_mdlist.add_widget(Bank_list_item(
				bankId = bank[0],
				bankName = bank[1],
				bankAccountCreatedAt = bank[3],
				bankAmount = str(bank[2]),
				icon = "bank"
			)
			)

class Edit_Bank_layout(MDBoxLayout):
	"""
	Edit bank info 
		This is going to be called by mddialog in BankList item as content_cls
	"""
	ToDay = date.today()
	def __init__(self, bankId) -> None:
		super(Edit_Bank_layout, self).__init__(bankId)
		self.bankId = bankId

		"""
		This is to change the text of the MDTextField when mddialog open
		"""
		bank = database.detailBankAccId(self.bankId)
		print(bank)
		self.bankEName.text = bank[1]
		self.bankEAmount.text = str(bank[2])
		self.bankECreatedAt.text = bank[3]

	def saveChanges(self):
		"""
		to save(update) changes to database
		"""
		updatedAt = date.today()
		database.updateBankAcc(self.bankId, self.bankEName.text, self.bankEAmount.text, self.bankECreatedAt.text, updatedAt)
		toast("Data is updated successfully")

class New_Bank_layout(MDBoxLayout):
	"""
	Adding New Bank Account
	"""
	ToDay = date.today()
	def __init__(self) -> None:
		super(New_Bank_layout, self).__init__()
	def addNewBank(self):
		"""
		Save Fixed Expense
		"""
		if self.bankName.text and self.bankAmount.text and self.bankCreatedAt.text:
			database.insertBankAcc(str(self.bankName.text), self.bankAmount.text, str(self.bankCreatedAt.text), str(self.bankCreatedAt.text))
			toast("Data saved now you can close")
		else:
			toast("Fill all the information")	



class New_Var_Expense_layout(MDBoxLayout):
	"""
	PopUP window to add new variable expenses
	"""
	def __init__(self) -> None:
		super(New_Var_Expense_layout, self).__init__()
	def addNewVarExpense(self):
		"""
		Save Fixed Expense
		"""
		if self.varExpenseItem.text and self.varExpenseAmount.text and self.varExpenseDate.text:
			type = "Variable"
			database.insertXpense(type, str(self.varExpenseItem.text), str(self.varExpenseAmount.text), str(self.varExpenseDate.text))
			toast("Data saved now you can close")
		else:
			toast("Fill all the information")	


class New_FExpense_layout(MDBoxLayout):
	"""
	PopUp window to add new fixed expenses
	"""
	def __init__(self) -> None:
		super(New_FExpense_layout, self).__init__()
	def addNewFExpense(self):
		"""
		Save Fixed Expense
		"""
		if self.fExpenseItem.text and self.fExpenseAmount.text and self.fExpenseDate.text:
			type = "Fixed"
			database.insertXpense(type, str(self.fExpenseItem.text), str(self.fExpenseAmount.text), str(self.fExpenseDate.text))
			toast("Data saved now you can close")
		else:
			toast("Fill all the information")

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

class New_sales_layout(MDBoxLayout):
	"""
	PopUp window to add new sales
	"""
	def __init__(self) -> None:
		super(New_sales_layout, self).__init__()
	def addNewSales(self):
		"""
		When Add button pressed in the new customer dialog
		"""
		if self.item_id.text and self.customer_id.text and self.item_quantitiy.text and self.sold_date.text and self.way_of_payment.text and self.bank_name.text and self.sales_revenue.text:
			#print(self.customer_bank_account_number.text)
			database.insertSales(self.item_id.text, self.customer_id.text, self.item_quantitiy.text, self.sold_date.text, self.way_of_payment.text, self.sales_revenue.text, self.bank_name.text)
			# to update customer frequencyOfPurchase and totalPurchase
			customer = database.deatilCustomer(self.customer_id)
			database.updateCustomer(self.customer_id, customer[1], customer[2], customer[3], customer[4], customer[5], customer[6], customer[7]+1, customer[8]+self.sales_revenue.text, customer[9])
			# to update bankAcc amount and updateAt
			bankAccount = database.detailBankAcc(self.bank_name.text)
			updateDate = date.today()
			updateDateStr = updateDate.strftime("%d/%m/%y")
			database.updateBankAcc(bankAccount[0], bankAccount[1], bankAccount[2]+self.sales_revenue.text, bankAccount[3], updateDateStr)
			toast('Sales added to database now you can close')
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
	def on_enter(self):
		self.itemList = database.readSItem()
		for x in self.itemList:
			if x[2] <= 0:
				availability = ("alert-circle", [1, 0, 0, 1], "No item")			
			elif x[2] < 10:
				availability = ("alert", [255/256, 165/256, 0, 1], "less than 10")
			else:
				availability = ("checkbox-marked-circle", [39/256, 174/256, 96/256, 1], "Available")
			x.insert(2, availability)

		####THIS IS FOR THE STOCK TAB TO LOAD THE MDDataTable AND Buttons####

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

		#####################################################
		####THIS FOR STOCK TAB TO LOAD THE CUSTOMER CARDS####

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

		####################################################
		#####THIS FOR SALES TAB TO LOAD THE CUSTOM TABLE####

		self.salesTab.clear_widgets()
		# here to made filter based on month
		allSales = database.readSomeSales()
		itemName=[]
		# here what i do is to convert itemId to itemName
		
		for x in allSales:
			itemName.append(database.detailItem(x[0])[1])
		y = 0
		for x in allSales:
			x[0] = itemName[y]
			y += 1

		for x in allSales:
			self.salesTab.add_widget(MDSalesCard(
				salesName = str(x[0]),
				salesQty = str(x[1]),
				salesAmount = str(x[2]),
				salesDate = str(x[3])
			))

	def newSales(self):
		"""
		Adding new single sales to database
		"""
		self.dialogNewSales = MDDialog(
			title="New Sales",
			type="custom",
			auto_dismiss=False,
			content_cls=New_sales_layout(),
			buttons=[
				MDRaisedButton(
					text="Close",
					theme_text_color="Custom",
					on_press=self.closeNewSales
				),
			]
		)
		self.dialogNewSales.open()
	def closeNewSales(self, inst):
		"""
		close button in add new sales dialog
		"""
		self.dialogNewSales.dismiss()
		self.on_enter()

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

	'''def customerFunc(self):
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
			#self.customerTab.add_widget(customerCard)'''

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


class Expneses(MDScreen):
	"""
	Expense page
	"""
	def __init__(self, **kwargs):
		"""
		Drop down monthMenu
		"""
		super().__init__(**kwargs)
	def monthMenu_callback(self, selMonth):
		"""
		When month selected
		"""
		self.monthDropDownMenuCaller.text=selMonth

	def on_enter(self):
		"""
		Whene entered to expenses
			# select name,amount,date from expenses (also check by type so type too)
		"""
		self.fixedExpenses.clear_widgets()
		self.variableExpenses.clear_widgets()
		# here to made filter based on month
		allExpense = database.readSomeExpenses
		fixed = []
		variable = []
		print(allExpense)

		for x in allExpense():
			if x[0] == 'Fixed':
				fixed.append(x)
			else:
				variable.append(x)

		for x in fixed:
			self.fixedExpenses.add_widget(MDXpense(
				expenseName = str(x[1]),
				expenseAmount = str(x[2]),
				expenseDate = str(x[3])
			))

		for x in variable:
			self.variableExpenses.add_widget(MDXpense(
				expenseName = str(x[1]),
				expenseAmount = str(x[2]),
				expenseDate = str(x[3])
			))
		##################
		months=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
		monthMenu_items = [
			{
				"viewclass": "OneLineListItem",
				"text": f"{i}",
				"height": dp(33),
				"on_release": lambda x=f"{i}": self.monthMenu_callback(x)
			}for i in months
		]
		self.main_monthMenu = MDDropdownMenu(
			items=monthMenu_items,
			caller=self.monthDropDownMenuCaller,
			width_mult=1.5,
		)

	def addFixedE(self):
		"""
		Add Fixed Expense
		so here we mddialog where other expense details filled
			except for the type that since that is fixed
		"""
		self.dialogNewFExpense = MDDialog(
			title="New Fixed Expense",
			type="custom",
			auto_dismiss=False,
			content_cls=New_FExpense_layout(),
			buttons=[
				MDRaisedButton(
					text="Close",
					theme_text_color="Custom",
					on_press=self.closeNewFExpense
				),
			]
		)
		self.dialogNewFExpense.open()

	def addVarE(self):
		"""
		Add Fixed Expense
		so here we mddialog where other expense details filled
			except for the type that since that is fixed
		"""
		self.dialogNewVarExpense = MDDialog(
			title="New Variable Expense",
			type="custom",
			auto_dismiss=False,
			content_cls=New_Var_Expense_layout(),
			buttons=[
				MDRaisedButton(
					text="Close",
					theme_text_color="Custom",
					on_press=self.closeNewVarExpense
				),
			]
		)
		self.dialogNewVarExpense.open()


	def closeNewFExpense(self, inst):
		self.dialogNewFExpense.dismiss()
		self.on_enter()

	def closeNewVarExpense(self, inst):
		self.dialogNewVarExpense.dismiss()
		self.on_enter()

class Setting(MDScreen):
	"""
	Settings page
	"""
	def bankList(self):
		self.dialogBankList = MDDialog(
			title="Bank list",
			type="custom",
			auto_dismiss=False,
			content_cls=Bank_list_layout(),
			buttons=[
				MDRaisedButton(
					text="Close",
					theme_text_color="Custom",
					on_press=self.closeBankList
				),
				MDRaisedButton(
					text="New",
					theme_text_color="Custom",
					on_press=self.newBank
				),

			]
		)

		self.dialogBankList.open()

	def closeBankList(self, *args):
		print("dismiss")
		self.dialogBankList.dismiss(force=True)

	def newBank(self, inst):
		"""
		New Bank MDDialog
		"""
		self.dialogBankList.dismiss()
		self.dialogNewBank = MDDialog(
			title="New Bank",
			type="custom",
			auto_dismiss=False,
			content_cls=New_Bank_layout(),
			buttons=[
				MDRaisedButton(
					text="Close",
					theme_text_color="Custom",
					on_press=self.closeNewBank
				),
			]
		)
		self.dialogNewBank.open()


	def closeNewBank(self, inst):
		self.dialogNewBank.dismiss()

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
		screen_manager.add_widget(Builder.load_file("home.kv"))
		screen_manager.add_widget(Builder.load_file("setings.kv"))
		screen_manager.add_widget(Builder.load_file("expenses.kv"))
		return screen_manager

	def backHome(self):
		"""
		This method is to go back to home
		"""
		self.root.transition.direction = "right"
		self.root.current = "home"

	def gotoSetting(self):
		"""
		to goto settings
		"""
		print('settings')
		self.root.transition.direction = "left"
		self.root.current = "setting"

if __name__ == "__main__":
	main().run()
