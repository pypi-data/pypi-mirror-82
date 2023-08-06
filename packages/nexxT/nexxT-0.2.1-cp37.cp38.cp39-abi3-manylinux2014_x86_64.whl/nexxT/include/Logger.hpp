/* 
 * SPDX-License-Identifier: Apache-2.0
 * Copyright (C) 2020 ifm electronic gmbh
 *
 * THE PROGRAM IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
 */

#ifndef NEXT_LOGGER_HPP
#define NEXT_LOGGER_HPP

#include "Services.hpp"
#include "NexTLinkage.hpp"
#include <QtCore/QMetaObject>

#define NEXT_LOG_LEVEL_NOTSET 0
#define NEXT_LOG_LEVEL_INTERNAL 5
#define NEXT_LOG_LEVEL_DEBUG 10
#define NEXT_LOG_LEVEL_INFO 20
#define NEXT_LOG_LEVEL_WARN 30
#define NEXT_LOG_LEVEL_ERROR 40
#define NEXT_LOG_LEVEL_CRITICAL 50

#ifdef AVOID_NAMESPACE
#define NEXT_LOG_INTERNAL(msg) log(NEXT_LOG_LEVEL_INTERNAL, msg, __FILE__, __LINE__)
#define NEXT_LOG_DEBUG(msg) Logging::log(NEXT_LOG_LEVEL_DEBUG, msg, __FILE__, __LINE__)
#define NEXT_LOG_INFO(msg) Logging::log(NEXT_LOG_LEVEL_INFO, msg, __FILE__, __LINE__)
#define NEXT_LOG_WARN(msg) Logging::log(NEXT_LOG_LEVEL_WARN, msg, __FILE__, __LINE__)
#define NEXT_LOG_ERROR(msg) Logging::log(NEXT_LOG_LEVEL_ERROR, msg, __FILE__, __LINE__)
#define NEXT_LOG_CRITICAL(msg) Logging::log(NEXT_LOG_LEVEL_CRITICAL, msg, __FILE__, __LINE__)
#else
#define NEXT_LOG_INTERNAL(msg) nexxT::Logging::log(NEXT_LOG_LEVEL_INTERNAL, msg, __FILE__, __LINE__)
#define NEXT_LOG_DEBUG(msg) nexxT::Logging::log(NEXT_LOG_LEVEL_DEBUG, msg, __FILE__, __LINE__)
#define NEXT_LOG_INFO(msg) nexxT::Logging::log(NEXT_LOG_LEVEL_INFO, msg, __FILE__, __LINE__)
#define NEXT_LOG_WARN(msg) nexxT::Logging::log(NEXT_LOG_LEVEL_WARN, msg, __FILE__, __LINE__)
#define NEXT_LOG_ERROR(msg) nexxT::Logging::log(NEXT_LOG_LEVEL_ERROR, msg, __FILE__, __LINE__)
#define NEXT_LOG_CRITICAL(msg) nexxT::Logging::log(NEXT_LOG_LEVEL_CRITICAL, msg, __FILE__, __LINE__)
#endif

START_NAMESPACE
    class DLLEXPORT Logging
    {
        static unsigned int loglevel;
        static void _log(unsigned int level, const QString &message, const QString &file, unsigned int line);
    public:
        static void setLogLevel(unsigned int level);
        static inline void log(unsigned int level, const QString &message, const QString &file, unsigned int line)
        {
            if( level >= loglevel )
            {
                _log(level, message, file, line);
            }
        }
    };
STOP_NAMESPACE

#endif
