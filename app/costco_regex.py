import re

def receipt_reader(receipt):
    # sample data, need to be replaced 
    #cosco_recpt = ["COSTCO","EWHOISALE","Mountain View #143", "1000 N Rengstorff","Mountain View, CA 94043","( 650 ) 988-1841","3Y Member 111855271732","***********Bottom of Basket**********","***********BOB Count 0 **************","251680 ORG RASPBERY 5.99","27003 STRAWBERRIES 6.99","1068080 PASTURE EGGS 749","647465 AVOCADOS 6CT 7.49","1057120 NORTHERN ** 19.79 A","SUBTOTAL 47.75","TAX 178","**** TOTAL L953","XXXXXXXXXXXX6364 SWIPED","Seq#: 10972 App#: 023125","Visa Resp: APPROVED","Tran ID#: 731500010972..","Merchant ID: 990143","APPROVED - Purchase","AMOUNT : $49.53","11/11/2017 16:04 143 10 291 67 49.53","CHANGE 0.00","Visa","A 9.0% TAX 1.78","TOTAL TAX 1.78","TOTAL NUMBER OF ITEMS SOLD = 5","IZII/2017 16:04 143 10 291 67","OP#: 67 Name: JENNIFER R.","Thank You!","Please Come Again","Whse:143 Trm:10 Trn:291 OP:67"]
    #cosco_recpt = ["COSTO","Livermore #146","2800 Independence Drive","Livermore, CA 94551","(9251 443-6306","8F Member 11186260269","*** MHMMMMM*Bottom of Basket*** MM MMM ***","446586 QUAKER OATS | 8.79","MMM MMM M*A**BOB Coont 1 MMX**********","1041 763 CEL PONCH 19.99 A","E 782294 POWER GREENS 4.49","E 826365 ORG. SQUASH 6.49","1027618 ORG TOR DAL 12.99","1109845 PERECT BAR 19.99","221177 SOCKEY SLMN 32.99","172246 ORG. CARROTS 4.79","563946 ORGANIC CHKN 19.99","42737 SHORT RIBS 33.85","121288 ORG BRNI MUSH 5.99","1068080 PASTURE EGGS 6.99","SUBTOTAL 177.34","TAX 1.85","**** TOTAL irA","XXXXXXXXXXXX6563 CHIP Read","AID: A0000000031010","Seq* 3830 Appt: 84001D","Visa Resp: APPROVED","Tran ID#: 727400003830/..","Merchant ID: 990146","APPROVED - Purchase","AMOUNT : $179.19","10/01/2017 16:14 146 3 243 15","Visa 179.19","CHANGE 0.00","A 9.25% TAX 1.85","TOTAL TAX 1.85","TOTAL NUMBER OF ITEMS SOLD - 12","10707201 16:14 146 3 243 15","OP#: 15 Name: Juan C","Thank You!","Please Come Again","Whse:146 Trm:3 Trn:243 OP:15","Total BOB Item Count - 1"]
 
    cosco_recpt = receipt
    items = []
    price = []
    item_price = [] 
    total = 0
    read_items_tag = 0
    payment = "Cash"
    json_output = {"AccountRef":{"value":"42","name":"Visa"},"PaymentType":"","Line":[{"Amount":"","DetailType":"AccountBasedExpenseLineDetail","AccountBasedExpenseLineDetail":{"AccountRef":{"name":"Meals and Entertainment","value":"13"}}}]}
    
    # iterate through the data (cosco_recpt)
    for line in cosco_recpt:
        per_item = {"Description":"","Amount":"","DetailType":"AccountBasedExpenseLineDetail","AccountBasedExpenseLineDetail":{"AccountRef":{"name":"Meals and Entertainment","value":"13"}}}
        # mark the beginning of item list 
        if bool(re.search("member\s+\S\d*",line, re.IGNORECASE)):
            read_items_tag = 1
            continue
        # read items/price pair and put in list for json object
        elif bool(re.search("\d+\s+(.*\D+)\s+(\d*\.\d{1,2}|\d+)", line, re.IGNORECASE)) and read_items_tag:
            m = re.search("\d+\s+(.*\D+)\s+(\d*\.\d{1,2}|\d+)",line)
            per_item["Amount"] = m.group(2)
            per_item["Description"] = m.group(1)
            item_price.append(per_item)
        # mark end of item list
        elif bool(re.search("SUBTOTAL\s*\d+\.\d+",line, re.IGNORECASE)):
            read_items_tag = 0
            continue
        # get total price
        elif bool(re.search("AMOUNT\s+:\s\$*(\d+\.\d+)",line, re.IGNORECASE)):
            total = re.search("AMOUNT\s+:\s\$*(\d+\.\d+)",line).group(1)
        elif bool(re.search("X{12}\d{4}", line, re.IGNORECASE)):
            payment = "CreditCard"
    json_output["PaymentType"] = payment
    json_output["Line"] = item_price
     
    #for debug purpose
    #print(json_output)
    return json_output
