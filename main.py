#!/usr/bin/python3
"""
STOCK managment
"""
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
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.metrics import dp
import os

class Tab(MDFloatLayout, MDTabsBase):
	"""
	Tab class
	"""
	pass

class store_window(MDScreen):
	"""
	store window class
	"""
	def on_enter(self):
		#layout = MDAnchorLayout()
		# for customers tab
		customer_tables = MDDataTable(
			pos_hint={'center_x': 0.5},
			size_hint=(1, 1),
			use_pagination=True,
			background_color_header="#65275a",
			elevation=3,
			rows_num=50,
			column_data=[
				("ID", dp(15)),
				("Company Name", dp(30), ),
		        ("Phone Number", dp(30)),
		        ("Tin Number", dp(30)),
		        ("Bank Account", dp(30)),],)
		    #row_data=[(f"{i + 1}", "C", "C++", "JAVA", "Python")for i in range(50)],)
		#layout.add_widget(data_tables)
		newCustomerFile = MDFloatingActionButton(
			icon="attachment",
			pos_hint={'x': .91, 'y': .08},
			on_release=self.uploadCustomerFromFile
			#md_bg_color=app.theme_cls.primary_color
		)#.bind(on_press=self.uploadCustomerFromFile)
		newCustomer = MDRectangleFlatIconButton(
			text="New",
			icon="plus",
			pos_hint={'x':.02, 'y': .05},
			on_release=self.newCustomer
			)#.bind(on_press=self.newCustomer)
		self.customers_tab.add_widget(customer_tables)
		self.customers_tab.add_widget(newCustomer)
		self.customers_tab.add_widget(newCustomerFile)

		# for stock tab
		stock_tables = MDDataTable(
			pos_hint={'center_x': 0.5},
			size_hint=(1, 1),
			use_pagination=True,
			#background_color_header="#65275a",
			elevation=3,
			rows_num=50,
			column_data=[
				("ID", dp(15)),
				("Item Name", dp(30), ),
		        ("Item Quantity", dp(24)),
		        ("Purchased Price", dp(25)),
		        ("Selling Price Single", dp(32)),
				("Selling Price Bulk", dp(31))],)
		    #row_data=[(f"{i + 1}", "C", "C++", "JAVA", "Python")for i in range(50)],)
		#layout.add_widget(data_tables)
		newStockFile = MDFloatingActionButton(
			icon="attachment",
			pos_hint={'x': .91, 'y': .08},
			#md_bg_color=app.theme_cls.primary_color,
			on_release=self.uploadStockFromFile
		)#.bind(on_press=self.uploadStockFromFile)
		newStock = MDRectangleFlatIconButton(
			text="New",
			icon="plus",
			pos_hint={'x':.02, 'y': .05},
			on_release=self.newStock
			)#.bind(on_press=self.newStock)
		self.stock_tab.add_widget(stock_tables)
		self.stock_tab.add_widget(newStock)
		self.stock_tab.add_widget(newStockFile)

		# salse tab
	def uploadCustomerFromFile(self, inst):
		"""
		to upload Customer data from XL file in specific format
			# open files and when specific file selected
			# check file extension
			# then check the format of the XL then
			# then travers data for each row and save it to database
			# then when all rows data are saved(til that show progress bar for user Interface) update MDDataTable
		"""
		path = os.path.expanduser("~")
		file_manager = MDFileManager(
			exit_manager=self.exit_manager,
			select_path=self.select_path,
			preview=True,
		)
		file_manager.show(path)

	def newCustomer(self, inst):
		"""
		Adding new single customer to database
			# first make popup
			# then to qualify and cahnge values type
			# then to insert into database by calling module `database.insertCustomer`
			# then update the MDDataTable
		"""

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
		file_manager = MDFileManager(
			exit_manager=self.exit_manager,
			select_path=self.select_path,
			preview=True,
		)
		file_manager.show(path)


	def newStock(self, inst):
		"""
		Adding new single customer to database
			# first make popup
			# then to qualify and cahnge values type
			# then to insert into database by calling module `database.insertCustomer`
			# then update the MDDataTable
		"""

	def select_path(self, path: str):
		'''
        It will be called when you click on the file name
        or the catalog selection button.

        :param path: path to the selected directory or file;
        '''

		self.exit_manager()
		toast(path)

	def exit_manager(self, *args):
		'''
		Called when the user reaches the root of the directory tree
		'''
		self.manager_open = False
		self.manager.dismiss()

class main(MDApp):
	"""
	main class
	"""
	currentTime = datetime.now()
	Hr = currentTime.hour
	#DEBUG = True
	#RAISE_ERROR = True
	#KV_DIRS = ["."]
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
