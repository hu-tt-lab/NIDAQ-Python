import Head from "next/head";
import Nav from "./Nav";
import { ReactNode } from "react";

type MainLayoutProps = {
  children: ReactNode;
};
const MainLayout = (props: MainLayoutProps) => {
  return (
    <>
      <Head>
        <title>Controller - Ultra Aquarius Next</title>
      </Head>
      <main className="bg-gray-800 h-full flex flex-col">{props.children}</main>
    </>
  );
};
export default MainLayout;
