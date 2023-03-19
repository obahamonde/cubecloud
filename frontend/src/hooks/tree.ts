import { SourceCodeFile } from "./types";

export const useTree = (files: SourceCodeFile[]) => {
  const groups: { [dir: string]: SourceCodeFile[] } = {};
  for (const file of files) {
    const parts = file.webkitRelativePath.split("/");
    const dir = parts.slice(0, -1).join("/");
    if (!groups[dir]) {
      groups[dir] = [];
    }
    groups[dir].push(file);
  }
  return groups;
};
