import Link from "next/link";
import { useRouter } from "next/router";
import { ReactNode } from "react";

type TabProps = {
  href: string;
  children: ReactNode;
};
const Tab = (props: TabProps) => {
  const path = useRouter().asPath;
  const selected = path.replace("home", "sessions") == props.href;
  return (
    <Link href={props.href}>
      <button className={selected ? "tab-selected" : "tab"}>
        {props.children}
      </button>
    </Link>
  );
};

type NavProps = {
  className?: string;
};
const Nav = (props: NavProps) => {
  return (
    <nav className={props.className}>
      <Tab href="/sessions">Sessions</Tab>
      <Tab href="/trains">Trains</Tab>
      <Tab href="/waveforms">Waveforms</Tab>
    </nav>
  );
};
export default Nav;
