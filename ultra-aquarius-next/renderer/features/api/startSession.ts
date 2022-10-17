import axios from "axios";
import { API_URL } from "./_constants";

export const startSession = async (session: string) => {
  const res = await axios.post(`${API_URL}/start_session`, {
    sessionName: session,
  });
  return res;
};
