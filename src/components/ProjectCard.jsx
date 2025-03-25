import { Card, CardBody, CardHeader, Image } from "@nextui-org/react";
import { useNavigate } from "react-router-dom";
import InProgressGif from "./../assets/in_progress.gif";
import { useState } from "react";
import VersionsList from "./VersionsList";

function darkenColor(color, percent) {
  const num = parseInt(color.slice(1), 16);
  const amt = Math.round(2.55 * percent);
  const R = (num >> 16) + amt;
  const G = ((num >> 8) & 0x00ff) + amt;
  const B = (num & 0x0000ff) + amt;

  return `#${(
    0x1000000 +
    (R < 255 ? (R < 1 ? 0 : R) : 255) * 0x10000 +
    (G < 255 ? (G < 1 ? 0 : G) : 255) * 0x100 +
    (B < 255 ? (B < 1 ? 0 : B) : 255)
  )
    .toString(16)
    .slice(1)
    .toUpperCase()}`;
}

function ProjectCard({
  color,
  text,
  description,
  link,
  technologies,
  enabled,
  versions = []
}) {
  // const backgroundColor = 'rgba(33,37,41, 0.03)'
  const textColor = 'black' //darkenColor(color, -40); // Darken by 20%
  const footerColor = darkenColor(color, -60); // Darken by 40%
  const navigate = useNavigate();
  const [showGif, setShowGif] = useState(false);

  return (
    <Card
      style={{
        border: `0.1rem solid ${textColor}`,
        boxShadow:
          "rgba(0, 0, 0, 0.16) 0px 10px 36px 0px, rgba(0, 0, 0, 0.06) 0px 0px 0px 1px",
      }}
      isPressable={enabled && versions.length == 0}
      className="w-[350px] h-[180px]"
      onPress={() => versions && versions.length > 0 ? {} : navigate(link)}
      onMouseEnter={() => setShowGif(true)}
      onMouseLeave={() => setShowGif(false)}
    >
      {showGif && !enabled
        ? <Image
          alt="Card background"
          className="object-cover rounded-xl opacity-100"
          src={InProgressGif}
          style={{ background: "white", width: "100%" }}
        /> : <>
          <CardHeader className="py-3 flex-col items-start text-left">
            <p
              style={{ color: textColor }}
              className="uppercase font-bold text-2xl text-left"
            >
              {text}
            </p>
            <h6
              className="font-medium text-md text-left"
              style={{ color: textColor, textTransform: "capitalize" }}
            >
              {description}
            </h6>
            {versions && versions.length > 0 && <VersionsList versions={versions} baseLink={link} />}
          </CardHeader>
          <CardBody
            className="absolute bottom-0 flex-col"
          >

            {technologies && technologies.length > 0 && (
              <h6 className=" text-sm" style={{ color: textColor }}>
                {technologies.join(", ")}
              </h6>
            )}
          </CardBody></>}

    </Card>
  );
}

export default ProjectCard;
