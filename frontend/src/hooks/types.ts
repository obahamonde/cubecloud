export type User = {
  sub: string;
  nickname?: string;
  name?: string;
  picture?: string;
  updated_at?: string;
  email?: string;
  email_verified?: boolean;
};

export type Notify = {
  message: string;
  status: string | number;
};

export type SourceCodeFile = {
  name: string;
  size: number;
  type: string;
  lastModified: number;
  lastModifiedDate: Date;
  key: string;
};

export type FileProps = {
  name: string;
  type: "file" | "directory";
  children?: Array<any> | null;
  content?: string;
  visible?: boolean;
};

export type FileNodeProps = {
  file: FileProps;
};
