
def getLogDailyReportModalJson(callback_id):
    model_data = {
                    "type": "modal",
                    "callback_id": callback_id,
                    "title": {
                        "type": "plain_text",
                        "text": "Daily Reporting App",
                        "emoji": True
                    },
                    "submit": {
                        "type": "plain_text",
                        "text": "Submit",
                        "emoji": True
                    },
                    "close": {
                        "type": "plain_text",
                        "text": "Cancel",
                        "emoji": True
                    },
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "Submit your reporting for the day!",
                                "emoji": True
                            }
                        },
                        {
                            "type": "actions",
                            "block_id": "project_channel",
                            "elements": [
                                {
                                    "type": "conversations_select",
                                    "placeholder": {
                                        "type": "plain_text",
                                        "text": "Select project channel",
                                        "emoji": True
                                    },
                                    "action_id": "actionId-0",
                                    "response_url_enabled": True,
                                    "default_to_current_conversation": True,
                                    # "initial_conversation": channel_id
                                }
                            ]
                        },
                        {
                            "type": "input",
                            "block_id": "what_have_you_done_today",
                            "element": {
                                "type": "plain_text_input",
                                "multiline": True,
                                "action_id": "plain_text_input-action"
                            },
                            "label": {
                                "type": "plain_text",
                                "text": "What you have done today?",
                                "emoji": True
                            }
                        },
                        {
                            "type": "input",
                            "block_id": "what_is_your_plan_for_tomorrow",
                            "element": {
                                "type": "plain_text_input",
                                "multiline": True,
                                "action_id": "plain_text_input-action"
                            },
                            "label": {
                                "type": "plain_text",
                                "text": "What your plan for tomorrow?",
                                "emoji": True
                            }
                        },
                        {
                            "type": "input",
                            "block_id": "any_blocker",
                            "element": {
                                "type": "plain_text_input",
                                "action_id": "plain_text_input-action",
                                "initial_value": "No"
                            },
                            "label": {
                                "type": "plain_text",
                                "text": "Any blocker?",
                                "emoji": True
                            }
                        }
                    ]
                }
    return model_data
    
def getLogScrumInfoModalJson(callback_id):
    model_data = {
                    "type": "modal",
                    "callback_id": callback_id,
                    "title": {
                        "type": "plain_text",
                        "text": "Daily Reporting App",
                        "emoji": True
                    },
                    "submit": {
                        "type": "plain_text",
                        "text": "Submit",
                        "emoji": True
                    },
                    "close": {
                        "type": "plain_text",
                        "text": "Cancel",
                        "emoji": True
                    },
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "Submit your meeting summary!",
                                "emoji": True
                            }
                        },
                        {
                            "type": "actions",
                            "block_id": "project_channel",
                            "elements": [
                                {
                                    "type": "conversations_select",
                                    "placeholder": {
                                        "type": "plain_text",
                                        "text": "Select project channel",
                                        "emoji": True
                                    },
                                    "action_id": "actionId-0",
                                    "response_url_enabled": True,
                                    "default_to_current_conversation": True
                                }
                            ]
                        },
                        {
            			"type": "input",
            			"block_id": "meeting_type",
            			"element": {
            				"type": "static_select",
            				"placeholder": {
            					"type": "plain_text",
            					"text": "Select Meeting Type",
            					"emoji": True
            				},
            				"options": [
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Daily Sync Meeting",
            							"emoji": True
            						},
            						"value": "Daily Sync Meeting"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Sprint Planning Meeting",
            							"emoji": True
            						},
            						"value": "Sprint Planning Meeting"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Project Demo Meeting",
            							"emoji": True
            						},
            						"value": "Project Demo Meeting"
            					}
            				],
            				"action_id": "static_select-action"
            			},
            			"label": {
            				"type": "plain_text",
            				"text": "Meeting Type",
            				"emoji": True
            			}
            		},
                        {
                            "type": "input",
                            "block_id": "summary",
                            "element": {
                                "type": "plain_text_input",
                                "multiline": True,
                                "action_id": "plain_text_input-action"
                            },
                            "label": {
                                "type": "plain_text",
                                "text": "Summary",
                                "emoji": True
                            }
                        }
                    ]
                }
    return model_data
    
def getNewLeadModalJson(callback_id):
    model_data = {
            	"type": "modal",
            	"callback_id": callback_id,
            	"title": {
            		"type": "plain_text",
            		"text": "Pre Sales Lead",
            		"emoji": True
            	},
            	"submit": {
            		"type": "plain_text",
            		"text": "Submit",
            		"emoji": True
            	},
            	"close": {
            		"type": "plain_text",
            		"text": "Cancel",
            		"emoji": True
            	},
            	"blocks": [
            		{
            			"type": "header",
            			"text": {
            				"type": "plain_text",
            				"text": "Add a new lead",
            				"emoji": True
            			}
            		},
            		{
            			"type": "input",
            			"block_id": "client_name",
            			"element": {
            				"type": "plain_text_input",
            				"multiline": False,
            				"action_id": "plain_text_input-action"
            			},
            			"label": {
            				"type": "plain_text",
            				"text": "Client Name",
            				"emoji": True
            			}
            		},
            		{
            			"type": "input",
            			"block_id": "client_email",
            			"element": {
            				"type": "plain_text_input",
            				"multiline": False,
            				"action_id": "plain_text_input-action"
            			},
            			"label": {
            				"type": "plain_text",
            				"text": "Client Email",
            				"emoji": True
            			}
            		},
            		{
            			"type": "input",
            			"block_id": "lead_source",
            			"element": {
            				"type": "static_select",
            				"placeholder": {
            					"type": "plain_text",
            					"text": "Select Lead Source",
            					"emoji": True
            				},
            				"options": [
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Adalo",
            							"emoji": True
            						},
            						"value": "Adalo"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Partner Website",
            							"emoji": True
            						},
            						"value": "Partner Website"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Brilworks Website",
            							"emoji": True
            						},
            						"value": "Brilworks Website"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Clutch",
            							"emoji": True
            						},
            						"value": "Clutch"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Referral",
            							"emoji": True
            						},
            						"value": "Referral"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Others",
            							"emoji": True
            						},
            						"value": "Others"
            					}
            				],
            				"action_id": "static_select-action"
            			},
            			"label": {
            				"type": "plain_text",
            				"text": "Lead Source",
            				"emoji": True
            			}
            		},
            		{
            			"type": "input",
            			"block_id": "country",
            			"element": {
            				"type": "static_select",
            				"placeholder": {
            					"type": "plain_text",
            					"text": "Select country",
            					"emoji": True
            				},
            				"options": [
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "USA",
            							"emoji": True
            						},
            						"value": "USA"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "UK",
            							"emoji": True
            						},
            						"value": "UK"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Australia",
            							"emoji": True
            						},
            						"value": "Australia"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Canada",
            							"emoji": True
            						},
            						"value": "Canada"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Neitherland",
            							"emoji": True
            						},
            						"value": "Neitherland"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Germany",
            							"emoji": True
            						},
            						"value": "Germany"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "UAE",
            							"emoji": True
            						},
            						"value": "UAE"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Spain",
            							"emoji": True
            						},
            						"value": "Spain"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "France",
            							"emoji": True
            						},
            						"value": "France"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Israel",
            							"emoji": True
            						},
            						"value": "Israel"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "India",
            							"emoji": True
            						},
            						"value": "India"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Asia",
            							"emoji": True
            						},
            						"value": "Asia"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Europe",
            							"emoji": True
            						},
            						"value": "Europe"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Others",
            							"emoji": True
            						},
            						"value": "Others"
            					}
            				],
            				"action_id": "static_select-action"
            			},
            			"label": {
            				"type": "plain_text",
            				"text": "Country/region",
            				"emoji": True
            			}
            		},
            		{
            			"type": "input",
            			"block_id": "project_type",
            			"element": {
            				"type": "static_select",
            				"placeholder": {
            					"type": "plain_text",
            					"text": "Select project type",
            					"emoji": True
            				},
            				"options": [
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Fixed",
            							"emoji": True
            						},
            						"value": "Fixed"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "Dedicated Resource",
            							"emoji": True
            						},
            						"value": "Dedicated Resource"
            					}
            				],
            				"action_id": "static_select-action"
            			},
            			"label": {
            				"type": "plain_text",
            				"text": "Project Type",
            				"emoji": True
            			}
            		},
            		{
            			"type": "input",
            			"block_id": "company",
            			"element": {
            				"type": "plain_text_input",
            				"action_id": "plain_text_input-action"
            			},
            			"label": {
            				"type": "plain_text",
            				"text": "Company",
            				"emoji": True
            			}
            		},
            		{
            			"type": "input",
            			"block_id": "linkedin",
            			"element": {
            				"type": "plain_text_input",
            				"action_id": "plain_text_input-action"
            			},
            			"label": {
            				"type": "plain_text",
            				"text": "LinkedIn",
            				"emoji": True
            			}
            		},
            		{
            			"type": "divider"
            		},
            		{
            			"type": "input",
            			"block_id": "description",
            			"element": {
            				"type": "plain_text_input",
            				"multiline": True,
            				"action_id": "plain_text_input-action"
            			},
            			"label": {
            				"type": "plain_text",
            				"text": "Description",
            				"emoji": True
            			}
            		},
            		{
            			"type": "input",
            			"block_id": "next_step",
            			"element": {
            				"type": "rich_text_input",
            				"action_id": "rich_text_input-action"
            			},
            			"label": {
            				"type": "plain_text",
            				"text": "Next Step",
            				"emoji": True
            			}
            		}
            	]
            }
    return model_data
