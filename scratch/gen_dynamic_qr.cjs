
const fs = require('fs');
const qrCodeJs = fs.readFileSync('scratch/qrcode.min.js', 'utf-8');
eval(qrCodeJs);
const qr = qrcode(0, 'M');
const payload = 'RR No ;AuthCode -;TDate -;TTime-cardType-cardname -GST IN NO -27AABCD5534A1Z5;HSN -996331;Invoice No-P720W00712;Date & Time08/14/26 1:15:20 PM;Items -4;Mode of Payment -Cash-0;Total-958.78;SGST-22.83CGST-22.83';
qr.addData(payload);
qr.make();
const tag = qr.createImgTag(4, 4);
const b64 = tag.slice(tag.indexOf('src="') + 5, tag.lastIndexOf('"')).split(',')[1];
fs.writeFileSync('scratch/dynamic_qr.gif', Buffer.from(b64, 'base64'));
