import { converters } from '@/constants';
import { Select, SelectItem } from '@heroui/react';

interface FormInputProps {
    onChange: any;
    value: Set<string>;
    name: string;
    errors: any;
    placeholder: string;
    isRequired?: boolean;
    label: string;
    disabled?:boolean;
}

const ConverterSelect = ({ onChange, value, isRequired, name, errors, placeholder, label, disabled=false }: FormInputProps) => {
    return (
        <Select
            selectedKeys={value}
            isRequired={isRequired}
            variant="bordered"
            //labelPlacement="outside"
            name={name}
            isDisabled={disabled}
            disabled={disabled}
            placeholder={placeholder}
            onSelectionChange={(keys)=> {
                onChange(keys);
            }}
            style={{
                textTransform:"capitalize"
            }}
            // errorMessage={({ validationDetails }) => {
            //     if (validationDetails.valueMissing) {
            //         return "Please enter country";
            //     }

            //     return errors.name;
            // }}
            label={label}
        >
            {converters.map((item)=>( <SelectItem key={item} value={item}>
                {item}
            </SelectItem>))}
           
        
        </Select>
    );
};

export default ConverterSelect;
