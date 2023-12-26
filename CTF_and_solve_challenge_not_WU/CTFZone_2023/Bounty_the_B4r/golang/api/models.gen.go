// Package api provides primitives to interact with the openapi HTTP API.
//
// Code generated by github.com/deepmap/oapi-codegen version v1.12.4 DO NOT EDIT.
package api

// AuthToken defines model for AuthToken.
type AuthToken struct {
	Token *string `json:"token,omitempty"`
}

// GenericResponse defines model for GenericResponse.
type GenericResponse struct {
	Error   *uint64 `json:"error,omitempty"`
	Message *string `json:"message,omitempty"`
}

// GetDiscoveryResponse defines model for GetDiscoveryResponse.
type GetDiscoveryResponse struct {
	Published *int64  `json:"published,omitempty"`
	Severity  *string `json:"severity,omitempty"`
	Title     *string `json:"title,omitempty"`
}

// GetProgramJoinedResponse defines model for GetProgramJoinedResponse.
type GetProgramJoinedResponse struct {
	Programs *[]string `json:"programs,omitempty"`
}

// GetProgramsResponse defines model for GetProgramsResponse.
type GetProgramsResponse = []Program

// GetReportResponse defines model for GetReportResponse.
type GetReportResponse struct {
	Description *string `json:"description,omitempty"`
	ProgramId   *string `json:"programId,omitempty"`
	ProgramName *string `json:"programName,omitempty"`
	Published   *int64  `json:"published,omitempty"`
	Severity    *string `json:"severity,omitempty"`
	Title       *string `json:"title,omitempty"`
	Weakness    *string `json:"weakness,omitempty"`
}

// ImportRepoRequest defines model for ImportRepoRequest.
type ImportRepoRequest struct {
	Username  *string `json:"username,omitempty"`
	Validator *string `json:"validator,omitempty"`
}

// JoinProgramResponse defines model for JoinProgramResponse.
type JoinProgramResponse struct {
	Success *string `json:"success,omitempty"`
}

// LoginRequest defines model for LoginRequest.
type LoginRequest struct {
	Password *string `json:"password,omitempty"`
	Username *string `json:"username,omitempty"`
}

// Program defines model for Program.
type Program struct {
	Id          *string `json:"id,omitempty"`
	Name        *string `json:"name,omitempty"`
	ProgramType *int    `json:"programType,omitempty"`
}

// SubmitReportRequest defines model for SubmitReportRequest.
type SubmitReportRequest struct {
	Description *string `json:"description,omitempty"`
	Program     *string `json:"program,omitempty"`
	Severity    *string `json:"severity,omitempty"`
	Title       *string `json:"title,omitempty"`
	Weakness    *string `json:"weakness,omitempty"`
}

// SubmitReportResponse defines model for SubmitReportResponse.
type SubmitReportResponse struct {
	ReportID *string `json:"reportID,omitempty"`
}

// UserInfoResponse defines model for UserInfoResponse.
type UserInfoResponse struct {
	Md5        *string `json:"md5,omitempty"`
	Pow        *string `json:"pow,omitempty"`
	Reputation *uint64 `json:"reputation,omitempty"`
	Username   *string `json:"username,omitempty"`
}

// GetReportRUuidParams defines parameters for GetReportRUuid.
type GetReportRUuidParams struct {
	// Pow Proof of work to let participants know that bruteforce is not an option
	Pow string `form:"pow" json:"pow"`
}

// PostReportJSONRequestBody defines body for PostReport for application/json ContentType.
type PostReportJSONRequestBody = SubmitReportRequest

// PostUserImportReputationJSONRequestBody defines body for PostUserImportReputation for application/json ContentType.
type PostUserImportReputationJSONRequestBody = ImportRepoRequest

// PostUserLoginJSONRequestBody defines body for PostUserLogin for application/json ContentType.
type PostUserLoginJSONRequestBody = LoginRequest

// PostUserRegisterJSONRequestBody defines body for PostUserRegister for application/json ContentType.
type PostUserRegisterJSONRequestBody = LoginRequest
