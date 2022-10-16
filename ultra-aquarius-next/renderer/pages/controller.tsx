import React from "react";
import { FlexCol, FlexRow } from "../components";
import ControllerLayout from "../layouts/ControllerLayout";

function Controller() {
  const sessions = ["session1", "session2"];
  const progress = 70;
  return (
    <ControllerLayout>
      <FlexCol className="h-full m-auto w-3/4 justify-evenly items-center">
        <h1 className="w-max text-2xl font-bold">Controller</h1>
        <FlexRow className=" w-full items-center justify-between">
          <div className="mr-2">Session</div>
          <select
            id="session-select"
            className="ml-2 px-1 py-0.5 flex-1 bg-gray-700 border-2 border-gray-600 rounded"
          >
            {sessions.map((session) => (
              <option>{session}</option>
            ))}
          </select>
        </FlexRow>
        <FlexCol className="items-center justify-evenly w-full">
          <FlexRow className="w-full mb-8 justify-center items-center overflow-hidden">
            <div className="bg-gray-900 border-gray-700 border-2 w-full h-3 rounded-full overflow-hidden">
              <div
                className="bg-cyan-600 w-full h-full rounded-full overflow-hidden relative"
                style={{ width: `${progress}%` }}
              >
                <div className=" bg-gradient-to-r from-transparent via-cyan-500 to-transparent w-14 h-full absolute top-0   animate-loop-right"></div>
              </div>
            </div>
            <div className="ml-3">{progress}%</div>
          </FlexRow>
          <FlexRow className="w-full justify-center">
            <button className="btn mr-2">start</button>
            <button className="btn-warning ml-2">stop</button>
          </FlexRow>
        </FlexCol>
      </FlexCol>
    </ControllerLayout>
  );
}

export default Controller;
