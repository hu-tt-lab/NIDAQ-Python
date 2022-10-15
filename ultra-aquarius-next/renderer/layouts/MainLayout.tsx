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
        <title>Ultra Aquarius Next</title>
      </Head>
      <section className="bg-gray-900 h-full flex flex-col">
        <Nav />
        <main className="bg-gray-800 flex-1 px-8 py-4">{props.children}</main>
      </section>
    </>
  );
};
export default MainLayout;
