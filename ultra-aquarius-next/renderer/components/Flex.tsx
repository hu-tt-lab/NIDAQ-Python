import { ReactNode } from "react";

export type FlexColProps = {
  children?: ReactNode;
  className?: string;
};
export const FlexCol = (props: FlexColProps) => {
  return (
    <div className={`flex flex-col ${props.className}`}>{props.children}</div>
  );
};
export type FlexRowProps = {
  children?: ReactNode;
  className?: string;
};
export const FlexRow = (props: FlexRowProps) => {
  return (
    <div className={`flex flex-row ${props.className}`}>{props.children}</div>
  );
};
