const cookieParser = require('cookie-parser')
const express = require('express')
const { exec } = require("child_process");
const qrcode = require('qrcode');

const PORT = process.env.PORT || 4560;

const app = express();
app.set('view engine', 'ejs');
app.use(express.json());
app.use(cookieParser());

class QRCode {
    constructor(value, defaultLength){
        this.value = value
        this.defaultLength = defaultLength
    }

    async getImage(){
        if(!this.value){
            // Use 'fortune' to generate a random funny line, based on the input size
            try {
                this.value = await execFortune(this.defaultLength)
            } catch (error) {
                this.value = 'Error while getting a funny line'
            }
        }
        return await qrcode.toDataURL(this.value).catch(err => 'error:(')
    }
}

app.get('/', async (req, res) => {
    res.render('index');
});

app.post('/generate', async (req, res) => {
    const { value } = req.body;
    try {
        let newQrCode;
        // If the length is too long, we use a default according to the length
        if (value.length > 150)
            newQrCode = new QRCode(null, value.lenght)
        else {
            newQrCode = new QRCode(String(value))
        }
        
        const code = await newQrCode.getImage()
        res.json({ code, data: newQrCode.value });
    } catch (error) {
        res.status(422).json({ message: "error", reason: 'Unknow error' });
    }
});

function execFortune(defaultLength) {
    return new Promise((resolve, reject) => {
     exec(`fortune -n ${defaultLength}`, (error, stdout, stderr) => {
      if (error) {
        reject(error);
      }
      resolve(stdout? stdout : stderr);
     });
    });
   }

app.listen(PORT, async () => {
    console.log(`QR Code Generator is running on port ${PORT}`);
});