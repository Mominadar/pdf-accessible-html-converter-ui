import axios from "axios";
import { toast } from "react-toastify";

const BASE_URL = import.meta.env.VITE_SERVER_URL;
const BUCKET_NAME = import.meta.env.VITE_BUCKET_NAME;
const BUCKET_REGION = import.meta.env.VITE_BUCKET_REGION;

export const uploadFile = async (url: string, file: File) => {
    try {
        await axios.put(url, file, {
            headers: {
                'Content-Type': file.type,
            }
        });
    } catch (e) {
        console.log(e);
        toast.error("Something went wrong translating file. Try again!");
    }
};

export const getPdfUrl = (fileName: string) => {
    const url = `https://${BUCKET_NAME}.s3.${BUCKET_REGION}.amazonaws.com/${fileName}`
    return url
}

export const getFiles = async (user, token) => {
    const apiKey = ""; //getApiKey(token);
    try {
        const res = await axios.post(`${BASE_URL}?action=get-files`, {
            username: user
        }, {
            headers: {
                "x-api-key": apiKey,
                "Authorization": `Bearer ${token}`
            }
        });
        const files = res.data;
        return files;
    } catch (e) {
        console.log(e);
        throw e;
    }
};

export const uploadConfig = async (username: string, fileName:string, pdfUrl: string, converter: string) => {
    try {
        const res = await axios.post(`${BASE_URL}?action=upload-config`, {
            username: username,
            file_name: fileName,
            pdf_url: pdfUrl,
            converter: converter
        },
            //   {
            //     headers: {
            //       "x-api-key": apiKey,
            //       "Authorization": `Bearer ${token}`
            //     }
            //   }
        );

        console.log("resss", res);
    } catch (err) {
        console.log("err", err)
    }
}

export const convert = async (objectKey: string) => {
    try {
        const res = await axios.post(`${BASE_URL}?action=convert`, {
            object_key: objectKey
        },
            //   {
            //     headers: {
            //       "x-api-key": apiKey,
            //       "Authorization": `Bearer ${token}`
            //     }
            //   }
        );

        console.log("resss", res);
    } catch (err) {
        console.log("err", err)
    }
}


export const queueForConversion = async (username: string, fileName:string, pdfUrl: string, converter: string) => {
    try {
        const res = await uploadConfig(username, fileName, pdfUrl, converter);
        console.log("resss", res);
    } catch (err) {
        console.log("err", err)
    }
}