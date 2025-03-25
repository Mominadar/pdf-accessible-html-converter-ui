import { RiParentFill } from "react-icons/ri";
import { MdChildFriendly } from "react-icons/md";
import { PiCertificateFill } from "react-icons/pi";
import { BsPersonVcard } from "react-icons/bs";
import { IoShieldCheckmark } from "react-icons/io5";
import { ReactElement } from "react";
import men1 from "@/assets/men1.jpg";
import men2 from "@/assets/men2.jpg";
import men3 from "@/assets/men3.jpg";
import women1 from "@/assets/women1.jpg";
import women2 from "@/assets/women2.jpg";
import domtoimage from "dom-to-image";

export const converters = [
    "agentic",
    "mistral"
]

export const getEmail = () => {
    return  "mbabar@unicef.org";
}

export const initialData = {
    firstName: "",
    middleName: "",
    lastName: "",
    country: new Set([]),
    city: "",
    placeOfBirth: "",
    dateTimeOfBirth: new Date(),
    gender: "",
    weight: undefined
}

export type StepType = {
    title: string;
    id: number;
    key: string;
    description: string;
    icon: ReactElement<any, any>;
}

export const steps: StepType[] = [
    { id: 1, key: "identify-parent", title: "Identification Registry", description: "Get/Generate DID for parents", icon: <BsPersonVcard style={{ fontSize: "2rem" }} /> },
    { id: 2, key: "add-child", title: "Child Details", description: "Add details for child", icon: <MdChildFriendly style={{ fontSize: "2rem" }} /> },
    { id: 3, key: "add-parent", title: "Parent Details", description: "Add details for parents", icon: <RiParentFill style={{ fontSize: "2rem" }} /> },
    { id: 4, key: "issue", title: "Issue Certificate", description: "Issue Certificate", icon: <PiCertificateFill style={{ fontSize: "2rem" }} /> },
    { id: 5, key: "verify", title: "Verify Certificate", description: "Verify Certificate", icon: <IoShieldCheckmark style={{ fontSize: "2rem" }} /> }
]

export type RegistryEntry = {
    id: number;
    identityNumber: string;
    firstName: string;
    middleName: string;
    lastName: string;
    dateOfBirth: Date
    placeOfBirth: string;
    city: string;
    country: string;
    address: string;
    picture: string;
    did: string | undefined;
    gender: "male" | "female";
    status: "active" | "inactive";
}
export const didRegistryMockData: RegistryEntry[] = [
    {
        id: 1,
        identityNumber: '54433-2321993-4',
        firstName: "Michael",
        middleName: "",
        lastName: "Johnson",
        dateOfBirth: new Date(1985, 3, 12),
        placeOfBirth: "Avenue Hospital, Lenchester",
        city: "Boston",
        country: "United States",
        address: "123 Main Street, New York, NY 10001",
        picture: men1,
        did: "did:ethr:sepholia:0x46eB0725F2ceB41b915D3E421b1D94DF9dD28f8a",
        gender: "male",
        status: "active",
    },
    {
        id: 2,
        identityNumber: '54433-2321993-6',
        firstName: "Troy",
        middleName: "",
        lastName: "Bolton",
        dateOfBirth: new Date(1997, 5, 21),
        placeOfBirth: "Christin Hospital",
        city: "Chicago",
        country: "United States",
        address: "House 24, M Street, Chicago, C 333333",
        picture: men2,
        did: "did:ethr:sepholia:0xbCC6af1Fd9c183f3e573EB9E13d8137951cd001d",
        gender: "male",
        status: "active",
    },
    {
        id: 3,
        identityNumber: '54433-2321993-5',
        firstName: "Jake",
        middleName: "Will",
        lastName: "Samson",
        dateOfBirth: new Date(1962, 4, 12),
        placeOfBirth: "Chicago Med Hospital",
        city: "Chicago",
        country: "United States",
        address: "123 Wall Street, Chicago, C 345333",
        picture: men3,
        did: undefined,
        gender: "male",
        status: "active",
    },
    {
        id: 4,
        identityNumber: '54422-2321993-5',
        firstName: "Emily",
        middleName: "",
        lastName: "Colson",
        dateOfBirth: new Date(1982, 1, 12),
        placeOfBirth: "Chicago Med Hospital",
        city: "Chicago",
        country: "United States",
        address: "123 Wall Street, Chicago, C 345333",
        picture: women1,
        did: "did:ethr:sepholia:0xc9979C3B6a11448811016Bb2f669eEfDAa055CE3",
        gender: "female",
        status: "active",
    },
    {
        id: 5,
        identityNumber: '54411-2321993-5',
        firstName: "Sara",
        middleName: "",
        lastName: "Trenton",
        dateOfBirth: new Date(1972, 4, 12),
        placeOfBirth: "Owen Clark Hospital",
        city: "Amsterdam",
        country: "United States",
        address: "Apartment 302, PK Flats, L Street, Amsterdam, C 111111",
        picture: women2,
        did: "did:ethr:sepholia:0x19c7238a0eaC9752aeFa6790182e6c9E31B32dB6",
        gender: "female",
        status: "active",
    },
    {
        id: 6,
        identityNumber: '54433-2661443-5',
        firstName: "Cassandra",
        middleName: "Elton",
        lastName: "Dexter",
        dateOfBirth: new Date(2012, 1, 5),
        placeOfBirth: "Chicago Med Hospital",
        city: "Chicago",
        country: "United States",
        address: "House no. 4, Street 12, F Avenue, D 22222",
        picture: "",
        did: "did:ethr:sepholia:0x0F5B9647360965f9AB7F69e54BafB2F79eFaDdA6",
        gender: "female",
        status: "inactive",
    },
    {
        id: 7,
        identityNumber: '54434-4111993-5',
        firstName: "James",
        middleName: "Sam",
        lastName: "Carlyle",
        dateOfBirth: new Date(2008, 4, 12),
        placeOfBirth: "Chicago Med Hospital",
        city: "Chicago",
        country: "United States",
        address: "123 Wall Street, Chicago,  C 345333",
        picture: "",
        did: undefined,
        gender: "male",
        status: "inactive",
    },
    {
        id: 8,
        identityNumber: '52233-2321993-5',
        firstName: "Dexter",
        middleName: "",
        lastName: "Colton",
        dateOfBirth: new Date(2007, 1, 28),
        placeOfBirth: "BY Red Hospital",
        city: "Los Angeles",
        country: "United States",
        address: "House 34, Trenton Heights, LA,  C 222222",
        picture: "",
        did: undefined,
        gender: "male",
        status: "inactive",
    }
]

export const getAge = (birthDate: Date) => {
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();

    // Adjust if the birthday hasn't occurred yet this year
    const monthDiff = today.getMonth() - birthDate.getMonth();
    const dayDiff = today.getDate() - birthDate.getDate();

    if (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)) {
        age--;
    }

    return age;
}

export const getFullName = (input: any) => {
    const name = `${input?.firstName ?? ""} ${input?.middleName ?? ""} ${input?.lastName ?? ""}`;
    return name;
}

export async function downloadLargeDivAsPDF(divId: string) {
    try {
        const dataUrl = await domtoimage.toPng(document.getElementById(divId))
        let link = document.createElement('a');
        link.href = dataUrl;
        link.download = 'BirthCertificate.png';
        link.click();
    } catch (error) {
        console.error('Error capturing certificate:', error);
    } 
}
