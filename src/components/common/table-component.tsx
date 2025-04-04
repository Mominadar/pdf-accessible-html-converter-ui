import React from "react";

import { FaExternalLinkAlt } from "react-icons/fa";
import { toast } from "react-toastify";
import { RiDownload2Fill } from "react-icons/ri";
import axios from "axios";
import { Chip, Table, Pagination, TableHeader, TableColumn, TableBody, Spinner, TableRow, TableCell, Tooltip } from "@nextui-org/react";
import { timeSince } from "../../utils";
import { MdOutlineRefresh } from "react-icons/md";
import { convert } from "../../actions";

export default function TableComponent({ data, isLoading, emptyContent, accessToken }: { data: any, isLoading: boolean, emptyContent: string, accessToken: string }) {
  const [page, setPage] = React.useState(1);
  const rowsPerPage = 5;


  const pages = React.useMemo(() => {
    return data?.length ? Math.ceil(data.length / rowsPerPage) : 0;
  }, [data, rowsPerPage]);

  const items = React.useMemo(() => {
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;

    return data.slice(start, end);
  }, [page, data]);

  const loadingState = isLoading ? "loading" : "idle";

  const downloadConvertedDocument = async (getUrl: string, name: string) => {
    try {
      const response = await axios.get(getUrl, {
        responseType: "blob",
      });
      const file = response.data;
      const originalFileName = name;

      if (!originalFileName) {
        toast.error("Something went wrong translating file. Try again!");
        return;
      }

      let mimeType = "text/html";
      let extensionForDownload = ".html";

      const blob = new Blob([file], { type: mimeType });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      const originalFileNameWithoutExtension = originalFileName
        .split(".")
        .slice(0, -1)
        .join(".");

      a.download = `converted_${originalFileNameWithoutExtension}.${extensionForDownload}`;
      a.href = url;
      a.click();
      window.URL.revokeObjectURL(url);

    } catch (e) {
      console.log(e);
      toast.error("Could not download file. Completed documents are only available for a specified amount of time after completion. File may have expired and removed. Try translating file again!")
    }

  };

  const parseStatus = (status: string) => {
    return <Chip className="capitalize" size="sm" variant="flat" color={status == "done" ? "success" : status == "error" ? "danger" : "primary"} style={{ textTransform: "capitalize" }}>
      <span>{status == "in_progress" ? "In Progress" : status == "error" ? "Error. Try again" : "Completed"}</span>
    </Chip>
  }

  const parseConverter = (converter: string) => {
    return <Chip className="capitalize" size="sm" variant="flat" color={converter == "agentic" ? "secondary" : "primary"} style={{ textTransform: "capitalize" }}>
      <span>{converter == "agentic" ? "Agentic" : "Mistral"}</span>
    </Chip>
  }


  const renderCell = React.useCallback((user: any, columnKey: string, index: number) => {
    //@ts-ignore
    const cellValue = user[columnKey];
    switch (columnKey) {
      case "index":
        return (
          <div className="flex flex-col">
            <p className="text-bold text-sm capitalize text-default-400">{index + 1}</p>
          </div>
        );
      case "object_key":
        return (
          <div className="flex flex-col">
            <p className="text-bold text-sm capitalize text-default-400 underline" onClick={() => {
               window.open(user.get_url, "_blank");
              }}>{cellValue}</p>
          </div>
        );
      case "converter":
          return (<>
            {parseConverter(cellValue)}
          </>
          );
      case "created_at":
        return (
          <div className="flex flex-col">
            <p className="text-bold text-sm capitalize text-default-400">{timeSince(cellValue)}</p>
          </div>
        );
      case "last_modified_at":
        return (
          <div className="flex flex-col">
            <p className="text-bold text-sm capitalize text-default-400">{timeSince(cellValue)}</p>
          </div>
        );
      case "file_status":
        return (<>
          {parseStatus(cellValue)}
        </>
        );
      case "actions":
        return (
          <div className="flex gap-[1rem] items-center">
            <Tooltip content="Download html file">
              <p className="text-bold text-sm capitalize text-default-400" onClick={() => {
                downloadConvertedDocument(user.put_url, user.object_key)
              }}> <RiDownload2Fill fontSize={"1.2rem"} /></p>
            </Tooltip>
            <Tooltip content="View html file">
              <p className="text-bold text-sm capitalize text-default-400" onClick={() => {
                window.open(user.put_url, "_blank");
              }}> <FaExternalLinkAlt /></p>
            </Tooltip>
            <Tooltip content="Reconvert file">
              <p className="text-bold text-sm capitalize text-default-400" onClick={async () => {
                toast.success("Reconverting file");
                convert(user["object_key"], accessToken);
              }}> <MdOutlineRefresh fontSize={"1.2rem"} style={{ fontWeight: 900 }} /></p>
            </Tooltip>
          </div>
        );
      default:
        return cellValue;
    }
  }, [items, data]);

  const columnKeys = ["index", "object_key", "converter", "file_status", "created_at", "last_modified_at", "actions"];

  return (
    <Table
      aria-label="Example table with client async pagination"
      bottomContent={
        pages > 0 ? (
          <div className="flex w-full justify-center">
            <Pagination
              isCompact
              showControls
              showShadow
              color="secondary"
              page={page}
              total={pages}
              onChange={(page) => setPage(page)}
            />
          </div>
        ) : null
      }
      classNames={{
        wrapper: "min-h-[25rem] !shadow-[None] px-[0] no-colored-shadow",
      }}
    >
      <TableHeader>
        <TableColumn key="index">Sr No.</TableColumn>
        <TableColumn key="object_key">Document Name</TableColumn>
        <TableColumn key="object_key">Converter</TableColumn>
        <TableColumn key="file_status">Status</TableColumn>
        <TableColumn key="created_at">Created At</TableColumn>
        <TableColumn key="last_modified_at">Last Modified At</TableColumn>
        <TableColumn key="actions">actions</TableColumn>
      </TableHeader>
      <TableBody
        items={items ?? []}
        loadingContent={<Spinner />}
        loadingState={loadingState}
        emptyContent={emptyContent}
      >
        {items.map((item: any, index: number) => {
          return <TableRow key={item.id} style={{ borderRadius: "1rem", background: "white" }}>
            {columnKeys.map((columnKey) => (<TableCell key={`${item.id}${columnKey}`}>{renderCell(item, columnKey, ((page - 1) * rowsPerPage) + index)}</TableCell>))}
          </TableRow>
        })}
      </TableBody>
    </Table>
  );
}

