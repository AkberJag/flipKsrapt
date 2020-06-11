:warning: flipkart's code changed, so bugs may occure.


# FlipKsrapt
A python based data mining tool for extracting information from Flipkart. It can loop through a product category and individual products, and fetch information.
### What information it fetches?
1.	Name of the product.
2.	Price of the product. (selling price and the original price)
3.	Product Description.
4.	All the specifications along with the main heading.
5.	The average review given on a page.
6.	All the image links of the product listed by the seller.
7.	URL of the product page.
### How fetched information are stored?
we can get the information in CSV or json format or both, configure it in the config.py file.
### Usage:
1.	search a category in Flipkart eg: “smart phones” and copy the URL.
2.	run the `flipksrapt.py`
3.	paste the URL when prompted.
4.  choose the required output format.
		- 1 for csv only
		- 2 for json only
		- 3 for both csv and json.
5.	Wait... Seriously, you'll need to wait some time. [ depends on your internet speed ]
 License:
FlipKsrapt is released under [The MIT license (MIT)](http://opensource.org/licenses/MIT)
---
#### Todo:
-	Extract Original images from product page. [currently extracting the thumbnails]
