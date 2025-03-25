import { Spinner } from "@nextui-org/react";

function Loader () {
    return (<div style={{ height: "100vh", display: "flex", justifyContent: "center" }}>
        <Spinner />
    </div>);

};

export default Loader;