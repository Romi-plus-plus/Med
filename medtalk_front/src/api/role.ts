export interface Perm {
  id: int;
  name: string;
  desc: string;
  route: string;
  enabled: true;
}

export interface Role {
  id: int;
  name: string;
  enabled: boolean;
  perms: Perm[];
}
