import { ToastContainer } from "react-toastify";

export default function DefaultLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="relative flex flex-col h-screen w-[100%]">
        {children}
        <ToastContainer/>
    </div>
  );
}
