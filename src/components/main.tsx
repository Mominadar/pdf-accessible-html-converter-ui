import { SetStateAction, useState } from "react";
//@ts-ignore
import QrReader from "react-qr-scanner";
import FileInput from "./common/file-input";
import { RxReset } from "react-icons/rx";
import CountrySelect from "./converter-select";
import TableComponent from "./common/table-component";
import { convert, getPdfUrl, queueForConversion, uploadFile } from "../actions";
import { toast } from "react-toastify";
import { Button, Card, Divider, Input, semanticColors } from "@nextui-org/react";
import { generateFileNameForUser } from "../utils";

const Main = ({ data, loadFiles, isLoading, user, accessToken }) => {
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);
    const [pdfUrl, setPdfUrl] = useState("");
    const [converter, setConverter] = useState<Set<string>>(new Set());
    return (
        <Card style={{ width: "70%", paddingInline: "2rem", paddingTop: "2rem", margin: "0 auto", gap: 15, display: "flex", justifyContent: "center", flexDirection: "column", borderTop: `10px solid ${semanticColors.light.secondary[500]}` }}>
            <FileInput
                onChange={async (files: any[]) => {
                    try {
                        const file = files[0];
                        if (file) {
                            setUploadedFile(file);

                        }
                    } catch (err) {
                        console.log("err", err);
                    }

                }} />
            <div style={{ display: "flex", alignItems: "center", marginBlock: "2px", justifyContent: "start", gap: 20 }}>
                <Divider style={{ maxWidth: "47%" }} />
                <p>or</p>
                <Divider style={{ maxWidth: "47%" }} />
            </div>
            <Input
                onChange={(e) => {
                    setPdfUrl(e.target.value);
                }}
                name="qr-code"
                placeholder="Enter Pdf URL Manually"
                value={pdfUrl}
                isClearable
                onClear={()=>{
                    setPdfUrl("");
                }}
            />
            <CountrySelect value={converter}
                onChange={(value: SetStateAction<Set<string>>) => {
                    setConverter(value);
                 }}
                name="country"
                errors={null}
                placeholder="Select Converter"
                label="Converter" />

            <Button style={{ background: semanticColors.light.secondary[500], color: "white", width: "fit-content", paddingInline: "2rem" }} onPress={async () => {
                try {
                    if(uploadedFile && pdfUrl){
                        toast.error("Specify only one of the options, either upload file or enter Url.");
                        return;
                    }
                    const converterValue = converter.values().next().value;
                    if(!converterValue){
                        toast.error("Select a converter to proceed");
                        return;
                    }
                    
                    let fileUrl = "";
                    let fileName = ""
                
                    if (uploadedFile) {
                        fileName = generateFileNameForUser(uploadedFile.name);
                        const url = getPdfUrl(fileName);
                        await uploadFile(url, uploadedFile);
                        fileUrl = url;
                    }else if(pdfUrl){
                        fileUrl = pdfUrl;
                        fileName = generateFileNameForUser(new URL(fileUrl).pathname.split('/').pop() ?? "sample-pdf.pdf" );
                    }else {
                        toast.error("Specify one of the options, either upload file or enter Url.");
                        return;
                    }

                    await queueForConversion(user.email, fileName,  fileUrl, converterValue, accessToken);
                    toast.success("Queued file for conversion!");
                    if(pdfUrl){
                        convert(fileName, accessToken);
                    }
                    //load files after queuing
                    setTimeout(async ()=>{
                        await loadFiles();
                    },2000);
                } catch (err) {
                    console.log("Error",err);
                    toast.error("Something went wrong! Try again");
                }
            }}
            >
                Convert
            </Button>
            
            <div style={{display:"flex", width:"100%", alignItems:"center", justifyContent:"space-between"}}>
            <h1 style={{ fontWeight:"bolder", fontSize:"1.3rem"}}>Your Converted Documents</h1>
            <Button color="secondary" style={{width:"fit-content", padding:10, minWidth:"fit-content", borderRadius:"50%"}} onPress={loadFiles}>
              <RxReset style={{fontSize:"1.2rem"}}/>
                </Button> 
            </div>
            <TableComponent isLoading={isLoading} data={data} emptyContent="No files found" accessToken={accessToken} />
        </Card>
    );
};

export default Main;