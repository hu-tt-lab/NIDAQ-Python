import axios from "axios";
import { API_URL } from "./_constants";

export const stopSession = async () => {
  const res = await axios.get(`${API_URL}/stop_session`);
  return res;
};
