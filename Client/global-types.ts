export type ApiPromise<T = any> = {
    success: boolean;
    data: T;
    error?: string;
    errorType?: string; // For special error handling (e.g., account_deactivated)
};

export type AccountStatus = "active" | "inactive" ;

export type AuthenticatedUser = {
    username: string,
    email: string,
    _id: string,
    token: string,
    profileUrl: string,
    account_status: AccountStatus,
}
export type AccountType = "user" | "admin"
export type SignUpPayload = {
    username: string;
    email: string;
    password: string;
    accountType: AccountType
};
