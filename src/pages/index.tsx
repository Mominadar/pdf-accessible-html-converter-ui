
import DefaultLayout from "../layouts/default";
import { useEffect, useState } from "react";
import Main from "../components/main";
import { getFiles } from "../actions";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function IndexPage({ user, accessToken }) {
  const [files, setFiles] = useState([]);
  const [isLoading, setLoading] = useState(true);
  const loadFiles = async () => {
    try {
      setLoading(true);
      const userFiles = await getFiles(user.email, accessToken);
      //@ts-ignore
      setFiles(userFiles.sort((a: { last_modified_at: string }, b: { last_modified_at: string  }) => new Date(b.last_modified_at) - new Date(a.last_modified_at)));
    } catch (err) {
      console.log("err", err)
      toast.error("Could not load files!");
    } finally {
      setLoading(false);
    }

  }
  useEffect(() => {
    const load = async () => {
      await loadFiles()
    }
    load();
  }, [])
  return (
    <DefaultLayout>
      <section className="flex flex-col items-center justify-center gap-1 py-5">
        <div className="inline-block max-w-lg text-center justify-center">
          <span className={"tracking-tight inline font-semibold text-[2rem] lg:text-3xl leading-9"}>
            Convert PDFs to Accessible HTML
          </span>
        </div>
      </section>
      <div style={{ display: "flex", justifyContent: "start", alignItems: "start", width: "70%", margin: "auto", flexDirection: "column", gap: 5, marginBlock: 10 }}>
        <Main data={files} loadFiles={loadFiles} isLoading={isLoading} user={user} accessToken={accessToken} />
      </div>
    </DefaultLayout>
  );
}
